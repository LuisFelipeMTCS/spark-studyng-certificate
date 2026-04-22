import os
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-21-openjdk-amd64'
from pyspark import StorageLevel

from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import col, rand, lit, when

spark = SparkSession.builder \
    .appName("challenge 3") \
    .config("spark.driver.memory", "2g") \
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

    # .config("spark.executor.memory", "8g") \

N = 100_000_000


df = spark.range(N) \
    .withColumn("idade", (rand() * 80 + 18).cast("int")) \
    .withColumn("salario", (rand() * 10000 + 1000).cast("double")) \
    .withColumn("pais", when(rand() > 0.5, "Brasil").otherwise("EUA")) \
    .withColumn("genero", when(rand() > 0.5, "Masculino").otherwise("Feminino"))



df.cache()
# df.persist(StorageLevel.MEMORY_ONLY)

# df.persist(StorageLevel.MEMORY_AND_DISK_2)
print("Total de linhas:", df.count())



resultado = df.groupBy("pais", "genero") \
    .agg({"salario": "sum", "idade": "avg"}) \
    .orderBy("pais", "genero")

resultado.show()
df.show(10)
