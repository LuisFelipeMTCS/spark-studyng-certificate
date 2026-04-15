# Dia 2 — Catalyst Optimizer: Physical Plan, Predicate Pushdown e Column Pruning

## Objetivo

Entender como o Spark transforma uma query em um plano de execução otimizado, identificando duas das otimizações automáticas mais importantes: **Predicate Pushdown** e **Column Pruning**.

---

## Conceitos

### Catalyst Optimizer

O Catalyst é o motor de otimização de queries do Spark SQL. Ele recebe o plano lógico (o que você escreveu) e devolve um plano físico otimizado (o que será de fato executado), passando por 4 fases:

```
Unresolved Logical Plan
        ↓  (Analysis)
  Resolved Logical Plan
        ↓  (Optimization)  ← Catalyst age aqui
  Optimized Logical Plan
        ↓  (Planning)
     Physical Plan          ← o que df.explain() mostra
```

### Predicate Pushdown

Filtros (`where`/`filter`) são empurrados para **o mais perto possível da fonte de dados**, antes de qualquer join ou agregação. Isso reduz o volume de dados lidos desde o início.

**Sem pushdown:** lê 100M linhas → filtra → retorna 1k  
**Com pushdown:** lê apenas as 1k linhas relevantes direto do storage

### Column Pruning

O Spark lê **apenas as colunas usadas** na query, descartando o resto antes de carregar os dados em memória. Formatos colunares como Parquet e Delta se beneficiam diretamente disso.

---

## Desafio

1. Criar um DataFrame com múltiplas colunas a partir de um arquivo Parquet ou gerado sinteticamente
2. Aplicar filtros e selecionar apenas algumas colunas
3. Usar `df.explain(True)` para inspecionar os 4 planos (Parsed, Analyzed, Optimized, Physical)
4. Identificar nos logs onde aparecem:
   - `PushedFilters` → evidência do Predicate Pushdown
   - Ausência de colunas desnecessárias no Physical Plan → evidência do Column Pruning
5. Comparar o plano **com** e **sem** a otimização para ver a diferença

---

## Como ler o `explain(True)`

```python
df.filter(...).select(...).explain(True)
```

A saída tem 4 seções, leia de **baixo para cima** no Physical Plan:

| Seção | O que mostra |
|---|---|
| `== Parsed Logical Plan ==` | Exatamente o que você escreveu |
| `== Analyzed Logical Plan ==` | Após resolver nomes de colunas e tipos |
| `== Optimized Logical Plan ==` | Após o Catalyst aplicar as regras |
| `== Physical Plan ==` | O que será executado de verdade |

Procure por `PushedFilters: [...]` no Physical Plan — se aparecer, o pushdown funcionou.

---

## Referências

- [Spark SQL Catalyst Optimizer (Databricks blog)](https://www.databricks.com/glossary/catalyst-optimizer)
- [df.explain() docs](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.explain.html)
