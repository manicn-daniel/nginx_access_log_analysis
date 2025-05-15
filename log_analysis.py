from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, col, to_timestamp, window, avg, max

spark = SparkSession.builder \
    .appName("Access Log Analysis") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .getOrCreate()

log_file_path = "access.log"
logs_df = spark.read.text(log_file_path)

# Regex patterns
ip_pattern = r'^(\S+)'
timestamp_pattern = r'\[(.*?)\]'
method_pattern = r'"(\S+)\s(\S+)'
response_code_pattern = r'"\s(\d{3})'
size_pattern = r'\s(\d+)$'

# Extract fields
logs_df = logs_df.withColumn("IP", regexp_extract(col("value"), ip_pattern, 1)) \
    .withColumn("Timestamp", regexp_extract(col("value"), timestamp_pattern, 1)) \
    .withColumn("Method", regexp_extract(col("value"), method_pattern, 1)) \
    .withColumn("Resource", regexp_extract(col("value"), method_pattern, 2)) \
    .withColumn("ResponseCode", regexp_extract(col("value"), response_code_pattern, 1)) \
    .withColumn("ResponseSize", regexp_extract(col("value"), size_pattern, 1)) \
    .drop("value")

# Cast types
logs_df = logs_df.withColumn("ResponseSize", col("ResponseSize").cast("int"))
logs_df = logs_df.withColumn("Timestamp", to_timestamp(col("Timestamp"), "dd/MMM/yyyy:HH:mm:ss Z"))

# Output directory base
out_dir = "output"

# Response Code Distribution
response_code_dist = logs_df.groupBy("ResponseCode").count() \
    .withColumn("Percentage", (col("count") / logs_df.count()) * 100)
response_code_dist.write.mode("overwrite").csv(f"{out_dir}/response_code_distribution", header=True)

# Traffic Trends Over Time
traffic_trends = logs_df.groupBy(window(col("Timestamp"), "1 hour")).count()
# Flatten window struct
traffic_flat = traffic_trends.select(
    col("window.start").alias("WindowStart"),
    col("window.end").alias("WindowEnd"),
    col("count")
)
traffic_flat.write.mode("overwrite").csv(f"{out_dir}/traffic_trends", header=True)

# Error Rate
error_df = logs_df.filter(col("ResponseCode").startswith("4") | col("ResponseCode").startswith("5"))
total_requests = logs_df.count()
error_requests = error_df.count()
error_rate_percent = (error_requests / total_requests) * 100
spark.createDataFrame([(error_rate_percent,)], ["ErrorRatePercent"]) \
    .write.mode("overwrite").csv(f"{out_dir}/error_rate", header=True)

# Redirects
logs_df.filter(col("ResponseCode").startswith("3")) \
    .groupBy("ResponseCode").count() \
    .write.mode("overwrite").csv(f"{out_dir}/redirects", header=True)

# Top Client Errors
logs_df.filter(col("ResponseCode").startswith("4")) \
    .groupBy("ResponseCode", "Resource").count() \
    .orderBy(col("count").desc()) \
    .write.mode("overwrite").csv(f"{out_dir}/top_client_errors", header=True)

# Server Errors
logs_df.filter(col("ResponseCode").startswith("5")) \
    .groupBy("ResponseCode").count() \
    .write.mode("overwrite").csv(f"{out_dir}/server_errors", header=True)

# Heavy Traffic Endpoints
logs_df.groupBy("Resource").count() \
    .orderBy(col("count").desc()) \
    .limit(10) \
    .write.mode("overwrite").csv(f"{out_dir}/top_endpoints", header=True)

# Response Size Stats
logs_df.groupBy("ResponseCode").agg(
    avg("ResponseSize").alias("AvgResponseSize"),
    max("ResponseSize").alias("MaxResponseSize")
).write.mode("overwrite").csv(f"{out_dir}/response_size_stats", header=True)

# Top IPs
logs_df.groupBy("IP").count() \
    .orderBy(col("count").desc()) \
    .limit(10) \
    .write.mode("overwrite").csv(f"{out_dir}/top_ips", header=True)

# HTTP Method Distribution
logs_df.groupBy("Method").count() \
    .write.mode("overwrite").csv(f"{out_dir}/method_distribution", header=True)

spark.stop()
