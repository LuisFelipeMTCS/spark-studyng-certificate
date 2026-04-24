import os
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-21-openjdk-amd64'
from pyspark import StorageLevel

from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import col, rand, lit, when

spark = SparkSession.builder \
    .appName("challenge 4") \
    .config("spark.driver.memory", "4g") \
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

N = 100_000_000

df = spark.range(N) \
    .withColumn("idade", (rand() * 80 + 18).cast("int")) \
    .withColumn("salario", (rand() * 10000 + 1000).cast("double")) \
    .withColumn("pais", lit("Brasil"))

# foram 20 repaticoes
# df.write.format("parquet").mode("overwrite").save("output_default")

# foram 4 repaticoes
# df.coalesce(4).write.format("parquet").mode("overwrite").save("output_coalesce")

# foram 4 repaticoes
# df.repartition(4).write.format("parquet").mode("overwrite").save("output_repartition")

# para verificar se vale a pena usar o coalesce ou repartition, podemos usar o explain para ver o plano de execução
df.rdd.getNumPartitions()


df.explain(True)

print("=== COALESCE ===")
df.coalesce(4).explain(True)

print("=== REPARTITION ===")
df.repartition(4).explain(True)
