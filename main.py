import os
import logging
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import file_io_utils as fu
import random

logging.basicConfig()
logging.getLogger(__name__)


batch_duration_seconds = 5

sc = SparkContext.getOrCreate()
ssc = StreamingContext(sc, batch_duration_seconds)

curr_dir = fu.get_this_dir()
INPUT_DIR = 'streaming_input'
streaming_dir = os.path.join(curr_dir,INPUT_DIR)

lines = ssc.textFileStream(streaming_dir)
# counts = lines.flatMap(lambda line: line.split(" "))\
#           .map(lambda x: (x, 1))\
#           .reduceByKey(lambda x, y: x+y)
# counts.pprint()

# lines.pprint(5)
split_lines = lines.map(lambda  line: line.split(","))
# split_lines.pprint((5))
count_ = split_lines.count()
# count_.pprint()

single_list = split_lines.flatMap(lambda x:x)
# single_list.pprint(20)

single_list.countByValue().pprint()
single_list.\
    map(lambda x: (x, 1)).\
    countByValue().\
    pprint()

# split_lines.\
#     map(lambda x: ('key', x)).\
#     pprint()
#
# split_lines.\
#     map(lambda x: ('key', x)).\
#     flatMapValues(lambda x:x).\
#     pprint()

# split_lines.\
#     map(lambda x: (str(random.randint(1,3)), x)).\
#     groupByKey().\
#     reduce(lambda x, y: x+y).\
#     pprint()
#
# split_lines.\
#     map(lambda x: (str(random.randint(1,3)), x)).\
#     reduceByKey(lambda x, y: x+y).\
#     pprint()

split_lines.\
    map(lambda x: (str(random.randint(1,3)), x)).\
    flatMapValues(lambda x: x).\
    mapValues(lambda x: (x,1)).\
    reduceByKey(lambda x, y: x+y).\
    pprint()
    # mapValues(lambda x: (x,1)).\
    # pprint()

ssc.start()
ssc.awaitTermination()
