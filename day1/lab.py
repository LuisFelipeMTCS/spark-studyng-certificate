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

# --- Schema Evolution com mergeSchema ---

# 1) Cria um novo DF com uma coluna extra que não existe na tabela delta_long
from pyspark.sql.functions import lit

df_com_nome = spark.range(5).withColumn("nome", lit("spark"))

print("Schema do novo DF (tem coluna extra 'nome'):")
df_com_nome.printSchema()

# 2) Sem mergeSchema=True, este append quebraria com erro de schema incompatível
# df_com_nome.write.format("delta").mode("append").save("delta_long")  # ← ERRO

# 3) Com mergeSchema=True, o Delta aceita a nova coluna e evolui o schema
df_com_nome.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save("delta_long")

# 4) Lê de volta e mostra o schema evoluído
print("Schema da tabela delta_long após mergeSchema:")
spark.read.format("delta").load("delta_long").printSchema()

# Linhas antigas têm null na coluna 'nome', novas têm o valor
print("Amostra com a coluna nova (antigas ficam null):")
spark.read.format("delta").load("delta_long").orderBy("id").show(8)