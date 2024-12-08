from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, BooleanType, FloatType


spark = SparkSession.builder \
    .appName("BusOperationCount") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()


kafka_brokers = "localhost:9092"
kafka_topic = "linha_2678-10"

schema = StructType([
    StructField("p", StringType(), True),
    StructField("a", BooleanType(), True),
    StructField("ta", StringType(), True),
    StructField("py", FloatType(), True),
    StructField("px", FloatType(), True),
    StructField("sv", StringType(), True),
    StructField("is", StringType(), True)
])


raw_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_brokers) \
    .option("subscribe", kafka_topic) \
    .load()

decoded_stream = raw_stream.selectExpr("CAST(value AS STRING) as json_data")

parsed_stream = decoded_stream.select(
    from_json(col("json_data"), schema).alias("data"))

bus_stream = parsed_stream.select("data.*").filter(col("a") == True)


query = bus_stream.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
