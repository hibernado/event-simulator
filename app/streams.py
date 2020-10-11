import os
import asyncio

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
        make_dir(self.dir)
        super().__init__()

    def init_sim(self, sim):
        sim.put = self.write_rows

    async def write_rows(self, rows):
        file_name = fu.get_random_filename()
        print('write file: %s' % file_name)
        path = os.path.join(self.dir, file_name)
        loop = asyncio.get_event_loop()

        await loop.run_in_executor(None, fu.write_csv, path, rows, self.delim)
