from pyspark import SparkContext
from pyspark.streaming import StreamingContext

batch_duration_seconds = 5

sc = SparkContext.getOrCreate()
ssc = StreamingContext(sc, batch_duration_seconds)
