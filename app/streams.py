import os

from app import file_io_utils as fu
from app.file_io_utils import make_dir


class BaseStreamer:

    def __init__(self):
        super().__init__()

    def init_sim(self):
        raise NotImplementedError


class FileStreamer(BaseStreamer):
    freq = None
    dir = None

    def __init__(self, dir, freq, delim):
        self.dir = dir
        self.freq = freq
        self.delim = delim
        super().__init__()

    def init_sim(self, sim):
        sim.put = self.write_rows

    def write_rows(self, rows):
        make_dir(self.dir)
        file_name = fu.get_random_filename()
        print('write file: %s' % file_name)
        path = os.path.join(self.dir, file_name)
        fu.write_csv(path, rows, self.delim)
