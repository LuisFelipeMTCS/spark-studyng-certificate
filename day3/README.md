# Dia 3 — Gerenciamento de Memória: Storage vs Execution Memory

## Objetivo

Entender como o Spark divide e gerencia a RAM internamente, a diferença entre **Storage Memory** e **Execution Memory**, e o que acontece quando a memória acaba.

---

## Conceitos

### Unified Memory Model

Desde o Spark 1.6, a memória do executor é dividida em regiões:

```
┌─────────────────────────────────────────────┐
│               Memória do Executor            │
│                                             │
│  ┌─────────────┐   ┌─────────────────────┐  │
│  │  Reserved   │   │   Unified Memory    │  │
│  │   Memory    │   │    (60% do total)   │  │
│  │   (300MB)   │   │                     │  │
│  │   fixo      │   │  Storage | Execution│  │
│  └─────────────┘   │  (50/50 mas fluido) │  │
│                    └─────────────────────┘  │
│  ┌──────────────────────────────────────┐   │
│  │         User Memory (40%)            │   │
│  │  (UDFs, estruturas Python, etc.)     │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### Storage Memory

Usada para **cache de DataFrames** (`df.cache()`, `df.persist()`).

- Quando você cacheia um DataFrame, ele vai para cá
- Se não houver espaço, o Spark **evict** (expulsa) blocos mais antigos
- Configuração: `spark.memory.storageFraction` (padrão: 0.5)

### Execution Memory

Usada para **operações em andamento**: shuffles, joins, sorts, aggregations.

- É consumida e liberada durante a execução de cada task
- Se faltar memória, o Spark **spilla para disco** (lento, mas não falha)
- Pode tomar espaço do Storage Memory se precisar (e vice-versa)

### A chave: eles compartilham o mesmo pool

O modelo **Unified** significa que as duas regiões são fluidas — se o Execution precisar de mais, pode usar o espaço do Storage (expulsando cache), e vice-versa. Isso evita desperdício de memória ociosa.

---

## Configurações importantes

| Configuração | Padrão | O que controla |
|---|---|---|
| `spark.executor.memory` | `1g` | Total de memória do executor |
| `spark.memory.fraction` | `0.6` | % do total para Unified Memory |
| `spark.memory.storageFraction` | `0.5` | % do Unified reservado para Storage |
| `spark.executor.memoryOverhead` | `10%` | Memória fora da JVM (Python, overhead) |

---

## O que acontece quando a memória acaba?

| Situação | Comportamento |
|---|---|
| Storage cheio | Blocos de cache são expulsos (eviction) |
| Execution cheio | Dados spilled para disco |
| Tudo cheio | `OutOfMemoryError` — executor morre |

---

## Desafio

1. Criar um DataFrame grande e cachear com `df.cache()`
2. Forçar a materialização com `.count()`
3. Abrir a **Spark UI** (`http://localhost:4040`) → aba **Storage** e observar quanto de memória o cache está usando
4. Rodar uma agregação pesada e observar na aba **Executors** o campo **Spill (disk)**
5. Ajustar `spark.executor.memory` e `spark.memory.fraction` e comparar o comportamento

---

## Como ver na Spark UI

```
http://localhost:4040
├── Storage   → cache dos DataFrames (quanto ocupa, quantas partições)
└── Executors → memória usada, GC time, Spill to disk
```

---

## Referências

- [Spark Memory Management (Databricks)](https://www.databricks.com/blog/2015/05/28/project-tungsten-bringing-spark-closer-to-bare-metal.html)
- [Configurações de memória (docs oficiais)](https://spark.apache.org/docs/latest/configuration.html#memory-management)
