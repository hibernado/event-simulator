from datetime import datetime
from os.path import realpath

import mock

import app.file_io_utils as io


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
