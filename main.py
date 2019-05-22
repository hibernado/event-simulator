import os
import logging
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

logging.basicConfig()
logging.getLogger(__name__)

def make_dir_if_not_exists(path):
    try:
        os.mkdir(path)
    except FileExistsError as e:
        logging.debug('Streaming director already exits: %s', path)

batch_duration_seconds = 5

sc = SparkContext.getOrCreate()
ssc = StreamingContext(sc, batch_duration_seconds)

curr_dir = os.path.dirname(os.path.realpath(__file__))
INPUT_DIR = 'streaming_input'
streaming_dir = os.path.join(curr_dir,INPUT_DIR)
make_dir_if_not_exists(streaming_dir)

