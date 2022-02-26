import csv
import os
import tarfile


class TarGzWriter:
    def __init__(self, root_filename, n_row_max=7000, filename_int_pad=5):
        """ root_filename - str - root of the ingest files
            n_row_max - int
            filename_int_pad - int
        """
        self._root_filename = root_filename
        self._n_row_max = n_row_max
        self._filename_int_pad = filename_int_pad

        self._file_ctr = 0
        self._row_ctr = 0
        self._file = open(self._get_filename(), "wt")

    def add_row(self, row_as_list):
        """ row_as_list - list<str>
        """
        self._refresh_file()
        self._file.write(','.join(row_as_list))
        self._row_ctr += 1

    def close(self):
        self._file.close()
        with tarfile.open(f"{self._file.name}.tar.gz", "w:gz") as tar:
            tar.add(self._file.name)

    def _get_filename(self):
        return f"{self._root_filename}_{str(self._file_ctr).zfill(self._filename_int_pad)}.txt"

    def _refresh_file(self):
        if self._row_ctr > self._n_row_max:
            self.close()
            self._file_ctr += 1
            self._row_ctr = 0
            self._file = open(self._get_filename(), "wt")


def make_admin_import_files():
    this_dir = os.path.abspath(os.path.dirname(__file__))
    source_file = os.path.join(this_dir, "data.csv.tar.gz")
    with tarfile.open(source_file, "r") as tarf:
        for member in tarf.getmembers():  # should be a length 1 array
            with tarf.extractfile(member) as f:
                source_node_writer = TarGzWriter("import_source_nodes")
                target_node_writer = TarGzWriter("import_target_nodes")  # may contain some nodes from source_node_writer
                relationship_writer = TarGzWriter("import_relationships")

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
    make_admin_import_files()
