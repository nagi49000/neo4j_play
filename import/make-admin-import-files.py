import csv
import os
import tarfile

class TarGzWriter:
    def __init__(self, root_filename, n_row_max=7000, filename_int_pad=5):
        self._root_filename = root_filename
        self._n_row_max = n_row_max
        self._filename_int_pad = filename_int_pad

        self._file_ctr = 0
        self._row_ctr = 0
        self._file = None

    def _refresh_file(self):
        if self._row_ctr > self._n_row_max:
            self._file.close()

def make_admin_import_files():
    this_dir = os.path.abspath(os.path.dirname(__file__))
    source_file = os.path.join(this_dir, "data.csv.tar.gz")
    with tarfile.open(source_file, "r") as tarf:
        for member in tarf.getmembers():
            with tarf.extractfile(member) as f:
                l = f.readline().decode()
                not_first_row = False
                while l:
                    l_fields = l.split(",")
                    if not_first_row:
                        source_id = int(l_fields[0].strip('"'))
                        source_username = l_fields[1].strip('"')
                        targets_str = l_fields[-1].strip().lstrip("[").rstrip("]")
                        target_ids = [int(x.strip('"')) for x in targets_str.split(" ") if x]
                    not_first_row = True
                    l = f.readline().decode()

if __name__ == "__main__":
    make_admin_import_files()
