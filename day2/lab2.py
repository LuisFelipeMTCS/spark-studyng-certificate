import os
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-21-openjdk-amd64'

from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import col, rand, lit

spark = SparkSession.builder \
    .appName("challenge 2") \
    .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()




N = 100_000_000

# Criando um DataFrame com várias colunas e tipos de dados diferentes
df = spark.range(N) \
    .withColumn("idade", (rand() * 80 + 18).cast("int")) \
    .withColumn("salario", (rand() * 10000 + 1000).cast("double")) \
    .withColumn("pais", lit("Brasil"))




# df.printSchema()
# df.show(5)


# Predicate Pushdown
# Filtra Linhas
df.where(col('idade') > 30).show(5)
df.filter(col('idade') > 30).show(5)


# Column Pruning
# Filtra colunas
df.select("idade").where(col('idade') > 30).show(5)


# Explain do DataFrame completo (sem otimização visível)
print("=== SEM otimização ===")
df.explain(True)

# Explain com filtro + select (aqui o Catalyst age)
print("=== COM Column Pruning + Predicate Pushdown ===")
df.select("idade").where(col("idade") > 30).explain(True)

