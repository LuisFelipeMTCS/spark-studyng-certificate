# Desafio Dia 1: Otimização de Schemas e Evolução no Delta Lake

## Objetivo
Explorar na prática como a escolha do tipo de dado e a evolução de schemas impactam a performance e escalabilidade em projetos Spark/Delta Lake.

## Explicação Detalhada

### Por que Schema e Tipos de Dados Importam?
No Spark, o schema define os tipos de dados de cada coluna. Isso afeta diretamente:
- **Performance:** Tipos mais eficientes aceleram leitura, escrita e processamento.
- **Escalabilidade:** Tipos com maior capacidade (como Long) evitam problemas de overflow em grandes volumes.
- **Compatibilidade:** Um schema bem definido facilita a evolução dos dados ao longo do tempo.

#### Integer vs Long
- **Integer** (32 bits): suporta valores de -2 bilhões a +2 bilhões. Pode ser suficiente para poucos dados, mas em Big Data, IDs podem facilmente ultrapassar esse limite.
- **Long** (64 bits): suporta valores muito maiores (até 9 quintilhões). É o padrão para grandes volumes, pois evita erros de overflow e garante que o sistema continue funcionando mesmo com crescimento exponencial dos dados.

### O que é Evolução de Schema (Schema Evolution)?
Em ambientes reais, os dados mudam: novas colunas são adicionadas, tipos mudam, etc. O Delta Lake permite evoluir o schema de uma tabela sem perder dados antigos, usando a opção `mergeSchema`.
- Isso facilita a manutenção e a escalabilidade do seu data lake.
- Permite adicionar colunas sem recriar tabelas ou perder histórico.

### Por que medir tempo e tamanho?
- **Tempo de escrita/leitura:** Mostra o impacto do tipo de dado na performance.
- **Tamanho dos arquivos:** Tipos diferentes ocupam espaços diferentes em disco. Em escala, isso pode significar economia de armazenamento e custos.

### Resumo
Ao fazer este desafio, você vai perceber que:
- Decisões simples de modelagem (tipo de dado) têm grande impacto em performance e escalabilidade.
- O Delta Lake facilita a evolução do schema, tornando o pipeline de dados mais flexível e robusto.
- Medir e comparar resultados é essencial para tomar decisões técnicas fundamentadas.

Leia esta explicação antes de começar o desafio para entender o "porquê" de cada etapa!

---

## Desafio
1. **Crie um DataFrame Spark com 10 milhões de linhas** contendo uma coluna de IDs numéricos. Gere duas versões:
   - Uma com a coluna como `Integer`.
   - Outra com a coluna como `Long`.
2. **Salve ambos os DataFrames em tabelas Delta** (pode ser em pastas diferentes).
3. **Ative e teste o MergeSchema**: Adicione uma nova coluna em cada DataFrame e salve novamente usando a opção `mergeSchema`.
4. **Compare o tamanho dos arquivos e o tempo de escrita/leitura** entre Integer e Long.
5. **Responda:** Por que o tipo Long é preferível em escala?

## Entregáveis
- Código Spark (PySpark ou Scala) usado para gerar os dados e salvar as tabelas.
- Print ou anotação dos resultados de tempo/tamanho.
- Resposta explicativa sobre a escolha do tipo Long.

## Dica
- Use `df.write.format("delta").option("mergeSchema", "true")...` para testar a evolução de schema.
- Use `os.path.getsize` ou comandos do Spark para medir o tamanho dos arquivos.

---

> **Este desafio reforça conceitos cobrados em certificações e prepara para problemas reais de evolução de dados em ambientes de produção.**
