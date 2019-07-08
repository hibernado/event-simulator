from datetime import datetime
from os.path import realpath, join, isfile
from pathlib import Path

import mock

import app.file_io_utils as io


def test_get_tempdir():
    dir_ = io.get_temp_dir()
    assert Path(dir_).is_dir()


def test_get_this_dir():
    dir_ = io.get_this_dir('~/path_to/file.txt')
    expected = realpath('~/path_to')
    assert expected == dir_


@mock.patch('app.file_io_utils.now')
@mock.patch('app.file_io_utils.uuid.uuid4')
def test_method(mock_uuid4, mock_now):
    mock_uuid4.return_value = 'UUID4_STRING'
    mock_now.return_value = datetime(2019, 7, 8, 8, 38, 47, 117682)
    assert io.get_random_filename() == '2019-07-08--08-38-47--UUID4_STRING'


def test_get_now():
    now_ = io.now()
    assert isinstance(now_, datetime)


def test_make_and_delete_dir():
    dir_ = join(io.get_temp_dir(), 'make_and_delete_folder')
    assert io.make_dir(dir_)
    assert not io.make_dir(dir_)  # returns false if dir exists
    assert Path(dir_).is_dir()

    assert io.delete_dir(dir_)
    assert not Path(dir_).is_dir()
    assert not io.delete_dir(dir_)  # returns false if no dir exists


def test_write_and_delete_csv():
    path_ = join(io.get_temp_dir(), 'test_data.csv')
    rows = []
    io.write_csv(path_, rows)
    assert isfile(path_)
    io.delete_file(path_)
    assert not isfile(path_)
