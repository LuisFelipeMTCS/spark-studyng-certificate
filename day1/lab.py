import os
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-21-openjdk-amd64'

from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType

spark = SparkSession.builder \
    .appName("challenge 1") \
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()


N = 100_000_000

# DataFrame com coluna 'id' do tipo Long (que é o tipo padrão para a função range)
df_long = spark.range(N)

# DataFrame com coluna 'id' do tipo Integer
df_int = df_long.withColumn("id", df_long["id"].cast(IntegerType()))

df_long.printSchema() 
df_int.printSchema()

df_long.show(3)
df_int.show(3)

df_long.write.format("delta").mode("overwrite").save("delta_long")
df_int.write.format("delta").mode("overwrite").save("delta_int")