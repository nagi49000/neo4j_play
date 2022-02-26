import csv
import os
import tarfile
import zipfile


class TarGzWriter:
    def __init__(self, root_filename, n_row_max=1000000, filename_int_pad=5):
        """ root_filename - str - root of the ingest files
            n_row_max - int - max number of rows in a tar.gz file before starting a new file
            filename_int_pad - int - formatting for integer in tar.gz filenames

            Object for writing rows of data to a partitioned set of tar.gz files
        """
        self._root_filename = root_filename
        self._n_row_max = n_row_max
        self._filename_int_pad = filename_int_pad

        self._file_ctr = 0
        self._row_ctr = 0
        self._file = open(self._get_filename(), "wt")

    def add_row(self, row_as_list):
        """ row_as_list - list<str> - csv row to write to file

            adds the row of data to file as a csv row
        """
        self._refresh_file()
        self._file.write(','.join(row_as_list) + "\n")
        self._row_ctr += 1

    def close(self):
        """ be sure to call this after all processing, otherwise there may be data loss
        """
        self._file.close()
        with tarfile.open(f"{self._file.name}.tar.gz", "w:gz") as tar:
            tar.add(self._file.name)
        os.remove(self._file.name)
        self._file = None

    def _get_filename(self):
        return f"{self._root_filename}_{str(self._file_ctr).zfill(self._filename_int_pad)}.csv"

    def _refresh_file(self):
        if self._row_ctr > self._n_row_max:
            self.close()
            self._file_ctr += 1
            self._row_ctr = 0
            self._file = open(self._get_filename(), "wt")


def make_admin_import_files():
    """ takes a zip file of twitter data, and processes it to a bunch of tar.gz
        files that can be fed to neo4j-admin import
    """
    this_dir = os.path.abspath(os.path.dirname(__file__))
    source_file = os.path.join(this_dir, "data.csv.zip")
    with zipfile.ZipFile(source_file, "r") as z:
        for member in z.namelist():  # should be a length 1 array
            with open("import-source-nodes-headers.csv", "wt") as f:
                f.write("userId:ID,userName")
            with open("import-target-nodes-headers.csv", "wt") as f:
                f.write("userId:ID")
            with open("import-relationships-headers.csv", "wt") as f:
                f.write(":START_ID,:END_ID")
            source_node_writer = TarGzWriter("import-source-nodes")
            target_node_writer = TarGzWriter("import-target-nodes")  # may contain some nodes from source_node_writer
            relationship_writer = TarGzWriter("import-relationships")

            with z.open(member, "r") as f:
                l = f.readline().decode()
                not_first_row = False
                while l:  # loop over lines in file
                    l_fields = l.split(",")
                    if not_first_row:
                        source_id = l_fields[0].strip('"')
                        source_username = l_fields[1]  # string, so don't strip "
                        targets_str = l_fields[-1].strip().lstrip("[").rstrip("]")
                        target_ids = [x.strip('"') for x in targets_str.split(" ") if x]

                        source_node_writer.add_row([source_id, source_username])
                        for target_id in target_ids:
                            target_node_writer.add_row([target_id])
                            relationship_writer.add_row([source_id, target_id])
                    not_first_row = True
                    l = f.readline().decode()

            source_node_writer.close()
            target_node_writer.close()
            relationship_writer.close()

if __name__ == "__main__":
    # tested on Python 3.7.6
    make_admin_import_files()
