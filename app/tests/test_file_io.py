from os.path import realpath
import app.file_io_utils as io


def test_get_this_dir():
    dir_ = io.get_this_dir('~/path_to/file.txt')
    expected = realpath('~/path_to')
    assert expected == dir_
