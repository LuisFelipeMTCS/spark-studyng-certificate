# Dia 4 — Small File Problem: repartition vs coalesce e impacto no IO

## Objetivo

Entender por que arquivos pequenos degradam a performance no Spark, e quando usar `repartition` ou `coalesce` para controlar o número de partições e o impacto no IO.

---

## Conceitos

### Small File Problem

Cada arquivo gerado pelo Spark vira uma **task de leitura** no próximo job. Se você tem 10.000 arquivos de 1MB ao invés de 10 arquivos de 1GB:

```
10.000 arquivos → 10.000 tasks de abertura
                → 10.000 conexões ao storage
                → overhead de scheduling enorme
                → job lento mesmo com poucos dados
```

É um dos problemas mais comuns em pipelines de produção — especialmente em jobs que rodam com muitas partições e salvam em Delta/Parquet.

---

### Partições no Spark

Cada partição = 1 arquivo no disco (ao salvar) = 1 task (ao processar).

```
df com 200 partições → salva 200 arquivos
df com 4 partições   → salva 4 arquivos
```

O número padrão de partições após um shuffle é controlado por:
```python
spark.conf.set("spark.sql.shuffle.partitions", 200)  # padrão
```

---

### repartition

Redistribui os dados em N partições com **shuffle completo** — move dados entre executors.

```python
df.repartition(10)           # por número
df.repartition(10, "pais")   # por número + coluna (hash partitioning)
```

**Quando usar:**
- Aumentar partições (scale up)
- Distribuir dados de forma uniforme antes de um join pesado
- Particionar por coluna específica

**Custo:** alto — faz shuffle completo na rede.

---

### coalesce

Reduz partições **sem shuffle** — apenas combina partições existentes no mesmo executor.

```python
df.coalesce(4)  # reduz para 4 partições
```

**Quando usar:**
- Reduzir partições ao final do pipeline antes de salvar
- Evitar o Small File Problem no output
- Quando você só quer diminuir, nunca aumentar

**Custo:** baixo — sem shuffle, sem movimento de dados na rede.

---

### Comparação

| | `repartition` | `coalesce` |
|---|---|---|
| Shuffle | Sim | Não |
| Direção | Aumenta ou diminui | Só diminui |
| Distribuição | Uniforme | Pode ficar desbalanceada |
| Custo | Alto | Baixo |
| Uso principal | Antes de joins | Antes de salvar |

---

## Desafio

1. Criar um DataFrame grande e salvar **sem** controle de partições — observar quantos arquivos foram gerados
2. Salvar com `coalesce(4)` e comparar o número de arquivos
3. Salvar com `repartition(4)` e comparar com o `coalesce`
4. Usar `df.explain(True)` para ver que o `coalesce` não gera Exchange (shuffle) no Physical Plan, mas o `repartition` sim
5. Medir o tempo de cada abordagem com `time`

---

## Como ver o impacto

```python
import time

# Sem controle
t0 = time.time()
df.write.format("parquet").mode("overwrite").save("output_default")
print("Default:", time.time() - t0, "s")

# Com coalesce
t0 = time.time()
df.coalesce(4).write.format("parquet").mode("overwrite").save("output_coalesce")
print("Coalesce:", time.time() - t0, "s")
```

```bash
# Contar arquivos gerados
ls output_default/*.parquet | wc -l
ls output_coalesce/*.parquet | wc -l
```

---

## Referências

- [Spark Partitioning (docs oficiais)](https://spark.apache.org/docs/latest/rdd-programming-guide.html#parallelized-collections)
- [repartition vs coalesce (Databricks)](https://www.databricks.com/blog/2016/07/14/a-tale-of-three-apache-spark-apis-rdds-dataframes-and-datasets.html)
