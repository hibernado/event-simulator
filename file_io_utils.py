import os
import logging
import tempfile
import uuid
import datetime
import shutil
import csv


LOG = logging.getLogger(__name__)


def get_temp_dir():
    return tempfile.gettempdir()


def get_this_dir():
    return os.path.dirname(os.path.realpath(__file__))


def get_random_filename(add_timestamp=True):
    name_ = str(uuid.uuid4())
    if add_timestamp:
        now_ = datetime.datetime.now().strftime("%Y-%m-%d-%H%-M-%F")
    return '-'.join([now_,name_])


def delete_dir(path):
    try:
        shutil.rmtree(path)
    except FileNotFoundError as e:
        LOG.info('Directory does not exist: %s', path)


def make_dir(path):
    try:
        os.mkdir(path)
    except FileExistsError as e:
        LOG.info('Directory already exits: %s', path)


def write_csv(path, rows):
    with open(path, 'w') as file_handle:
        writer = csv.writer(file_handle)
        writer.writerows(rows)
    LOG.info('Write csv %s', path)


def delete_file(path):
    os.remove(path)
