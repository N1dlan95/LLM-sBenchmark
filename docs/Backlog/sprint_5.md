# Sprint 5 — Modelagem Estatística Completa, Aderência e Apresentação Final

- **Alinhamento (Segunda):** 21/12/2026
- **Entrega e Apresentação (Quarta):** 23/12/2026
- **Critério de Aceite:** `notebooks/relatorio_final.ipynb` executado sem erros com todas as modelagens discretas e contínuas, testes de aderência (QQ-plot, AIC/BIC, Qui-quadrado, KS), análise de superdispersão por dificuldade, gráficos/tabelas exportados e apresentação final pronta.

---

## Tasks por Membro

### Membro 1 (Engenharia de Coleta & API)
- **[S5-T1]** Congelar versão final do código de coleta e CLI, revisar `README.md` com instruções completas de reprodução do experimento e variáveis de ambiente.
- **[S5-T2]** Estruturar a seção técnica de **Arquitetura & Coleta de Dados** nos slides da apresentação final (fluxo de lotes de 20, medição com `perf_counter()` e resiliência com SQLite).

### Membro 2 (Curadoria & Auditoria de Dados)
- **[S5-T3]** Consolidar o relatório de **Metodologia, Curadoria e Auditoria** (composição das 300 perguntas, *system prompt*, viés do corretor medido nos 10% e ameaças à validade/limitações).
- **[S5-T4]** Preparar a seção de **Metodologia Experimental & Limitações** para a apresentação em sala e revisar a clareza textual do notebook final.

### Membro 3 (Banco de Dados, Corretor & Testes)
- **[S5-T5]** Executar e validar em `src/analytics/validation.py` os **testes de aderência e pressupostos**: Kolmogorov-Smirnov (KS), Qui-quadrado de aderência, cálculo de AIC/BIC e verificação de independência/homogeneidade entre lotes.
- **[S5-T6]** Implementar e executar o **teste/diagnóstico de superdispersão por nível de dificuldade** (comparando variância empírica da Binomial em lotes de 20 com $np(1-p)$ e estratificando por `fácil`, `média`, `difícil`).

### Membro 4 (Modelagem Estatística & Visualização)
- **[S5-T7]** Concluir a modelagem discreta em `src/analytics/discrete.py` e no notebook: **Binomial em lotes de 20 com Intervalo de Confiança de 95%**, **Geométrica** (tentativas até a 1ª alucinação) e **Binomial Negativa** (tentativas até a $r$-ésima alucinação).
- **[S5-T8]** Concluir a modelagem contínua em `src/analytics/continuous.py` e no notebook: ajustes **Normal**, **Exponencial deslocada** e **Log-Normal** para latência (`latency_ms`) e contagem de tokens (`output_tokens`).
- **[S5-T9]** Gerar e exportar em alta resolução (`docs/figuras/` ou `reports/figures/`) todos os gráficos e tabelas finais (**QQ-plots**, histogramas com curvas ajustadas, comparativo AIC/BIC, IC 95% por lote e taxa de falha por dificuldade).
- **[S5-T10]** Realizar execução limpa (*Restart & Run All*) de `notebooks/relatorio_final.ipynb` e montar os slides finais de resultados probabilísticos com a equipe.
