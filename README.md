# 📚 Deep Dive Spark Study Checklist

Este cronograma foi criado para preparação intensiva para a certificação Databricks/Spark, com foco em entender os detalhes internos, performance e Lakehouse. Checklist para marcar o progresso e anotar aprendizados. **Meu intuito aqui é mostrar como utilizar IA para auxiliar como ferramente e, não como cerebro**

---

## Semana 1: Internals & Query Optimization
- [X] **Dia 1:** Otimização de Schemas e Evolução (MergeSchema no Delta). Por que Long é melhor que Integer em escala?
- [X] **Dia 2:** Catalyst Optimizer: Analisar o Physical Plan (`df.explain(True)`). Identificar Predicate Pushdown e Column Pruning.
- [X] **Dia 3:** Gerenciamento de Memória: Como o Spark divide a RAM (Storage vs execution memory).
- [ ] **Dia 4:** Arquivos Pequenos (Small File Problem): Estratégias de repartition vs coalesce e o impacto no IO.
- [ ] **Dia 5:** Bucketing vs Partitioning: Quando usar cada um para evitar Shuffles em joins frequentes.
- [ ] **Dia 6:** AQE (Adaptive Query Execution): Entender Coalescing Post-shuffle Partitions e Skew Join Optimization.
- [ ] **Dia 7:** Simulado Técnico: Resolver problemas de código que falham por OutOfMemoryError.

## Semana 2: Joins de Elite & Performance
- [ ] **Dia 8:** Broadcast Hash Join: Limites, configurações e quando o Spark desiste de fazer broadcast.
- [ ] **Dia 9:** Sort Merge Join vs Shuffle Hash Join: A anatomia do movimento de dados na rede.
- [ ] **Dia 10:** Tratamento de Data Skew (Dados desbalanceados): Técnicas de Salting (salgamento de chaves).
- [ ] **Dia 11:** Window Functions Avançadas: `rangeBetween` vs `rowsBetween` para cálculos de séries temporais.
- [ ] **Dia 12:** UDFs vs Pandas UDFs (Vectorized): Por que UDFs Python são lentas e como o Apache Arrow resolve isso.
- [ ] **Dia 13:** Caching e Persistência: Diferença real entre MEMORY_ONLY, DISK_ONLY e OFF_HEAP.
- [ ] **Dia 14:** Spark UI Profissional: Identificar gargalos de CPU vs Rede olhando as métricas de Task Deserialization e Shuffle Read.

## Semana 3: Delta Lake & Lakehouse (Foco Certificação)
- [ ] **Dia 15:** ACID no Lake: Como o Transaction Log funciona por baixo dos panos.
- [ ] **Dia 16:** Time Travel e Vacuum: Gerenciamento de versões e retenção de dados.
- [ ] **Dia 17:** Schema Enforcement vs Schema Evolution: Como garantir a qualidade no Bronze/Silver.
- [ ] **Dia 18:** Z-Order vs Data Skipping: Aumentando a performance de leitura em 100x.
- [ ] **Dia 19:** Change Data Feed (CDF): Como capturar mudanças entre camadas de forma eficiente.
- [ ] **Dia 20:** Unity Catalog (Básico): Governança, linhagem e permissões (cai muito na prova nova).
- [ ] **Dia 21:** Projeto Rápido: Implementar uma camada Silver que trata duplicatas de forma incremental.

## Semana 4: Streaming & Preparação Final
- [ ] **Dia 22:** Structured Streaming: Trigger de Micro-batch vs Continuous Processing.
- [ ] **Dia 23:** Watermarking: Lidar com dados que chegam atrasados em eventos de streaming.
- [ ] **Dia 24:** State Management: O que acontece quando o checkpoint cresce demais.
- [ ] **Dia 25:** Integração Spark + Kafka: Estratégias de consumo e commits.
- [ ] **Dia 26-30:** Simulados e Revisão de Pesos: Focar nas "pegadinhas" da Databricks (ex: syntax de SQL vs Python no Spark).

---

## 🧪 Projeto de Estudo: Pipeline de Telemetria de Alta Performance
- [ ] Gerar 10 milhões de linhas com Skews propositais (um motorista com 50% dos dados).
- [ ] Implementar Salting para resolver join com tabela de metadados.
- [ ] Salvar em Delta Lake usando Z-Order na coluna de data e ID.
- [ ] Monitorar a Spark UI e provar que o tempo de execução caiu após as otimizações.


