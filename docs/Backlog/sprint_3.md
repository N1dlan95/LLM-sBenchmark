# Sprint 3 — Persistência Incremental, Coleta Piloto e Corretor Automático

- **Alinhamento (Segunda):** 07/12/2026
- **Entrega (Quarta):** 09/12/2026
- **Critério de Aceite:** `COMMIT` executado a cada requisição no SQLite; coleta piloto de 20 a 30 perguntas reais concluída sem perda de dados; corretor automático validado com ≥ 90% de concordância frente à conferência manual do piloto.

---

## Tasks por Membro

### Membro 1 (Engenharia de Coleta & API)
- **[S3-T1]** Alterar `src/pipeline/runner.py` para realizar `conn.commit()` imediatamente após cada inserção individual na tabela `responses` (persistência incremental por requisição, evitando perda de dados em quedas).
- **[S3-T2]** Implementar suporte a retomada (*resume*) de execução para pular perguntas já respondidas dentro de um mesmo `run_id` ou experimento interrompido.
- **[S3-T3]** Executar a **coleta piloto real** com 20 a 30 perguntas estratificadas por dificuldade, registrando horários, modelos e temperaturas configuradas.

### Membro 2 (Curadoria & Auditoria de Dados)
- **[S3-T4]** Realizar conferência manual integral (100%) das 20–30 respostas da coleta piloto aplicando a regra operacional (`1 = acerto`, `0 = falha`).
- **[S3-T5]** Catalogar padrões reais de resposta do modelo observados no piloto (ex.: pontuação extra, unidades de medida, respostas com explicação curta) para refinar sinônimos e o *system prompt* antes da coleta completa.

### Membro 3 (Banco de Dados, Corretor & Testes)
- **[S3-T6]** Implementar e aprimorar o corretor automático em `src/pipeline/evaluator.py` (`grader.py`) com pipeline de normalização de texto (remoção de acentos, pontuação, *casefolding*, espaços extras) e checagem contra `gabarito` + `sinonimos_aceitos`.
- **[S3-T7]** Criar teste automatizado simulando interrupção abrupta no meio de um lote para comprovar que as requisições anteriores já comitadas permanecem intactas no SQLite.
- **[S3-T8]** Comparar a saída do corretor automático com o gabarito manual do piloto (Membro 2) gerando matriz de confusão (verdadeiros positivos/negativos, falsos positivos/negativos) e taxa de concordância.

### Membro 4 (Modelagem Estatística & Visualização)
- **[S3-T9]** Executar uma análise exploratória preliminar dos dados do piloto (distribuição empírica da latência e tokens de saída; proporção inicial de acertos vs. falhas).
- **[S3-T10]** Validar a adequação da formatação dos lotes de 20 e das séries de falhas para alimentar `src/analytics/discrete.py` e `src/analytics/continuous.py`.
