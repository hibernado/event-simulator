import csv
import datetime
import logging
import os
import shutil
import tempfile
import uuid

LOG = logging.getLogger(__name__)


def get_temp_dir():
    return tempfile.gettempdir()


def get_this_dir(file_path=__file__):
    return os.path.dirname(os.path.realpath(file_path))


def now():
    return datetime.datetime.now()


def get_random_filename(add_timestamp=True):
    name_ = str(uuid.uuid4())
    if add_timestamp:
        now_ = now().strftime("%Y-%m-%d--%H-%M-%S")
    return '--'.join([now_, name_])


def delete_dir(path):
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        LOG.info('Directory does not exist: %s', path)


def make_dir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        LOG.info('Directory already exits: %s', path)


def write_csv(path, rows):
    with open(path, 'w') as file_handle:
        writer = csv.writer(file_handle)
        writer.writerows(rows)
    LOG.info('write csv %s', path)


def delete_file(path):
    os.remove(path)
