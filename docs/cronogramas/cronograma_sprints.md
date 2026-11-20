# Cronograma de Sprints — Modelagem Probabilística da Alucinação e da Incerteza em LLMs

- **Início do ciclo:** Segunda-feira, 23/11/2026
- **Entrega final e apresentação:** Quarta-feira, 23/12/2026
- **Rito de alinhamento (Weekly):** Toda segunda-feira em horário de aula (23/11, 30/11, 07/12, 14/12, 21/12)
- **Rito de entrega (Sprint Review):** Toda quarta-feira (25/11, 02/12, 09/12, 16/12, 23/12)

---

## Tabela Resumo das 5 Sprints

| Sprint | Alinhamento (Segunda) | Entrega (Quarta) | Foco Principal | Critério de Aceite (*Definition of Done*) |
| :--- | :--- | :--- | :--- | :--- |
| **Sprint 1** | 23/11/2026 | 25/11/2026 | Setup do repositório Python (`app.py` com `argparse` para `coletar`, `corrigir`, `analisar`), regra operacional (`1 = acerto`, `0 = falha`), *system prompt* curto, `.env` e pipeline ponta a ponta com dados simulados. | CLI executa `coletar`, `corrigir` e `analisar` sem erros usando dados simulados; `.env.example` e regra de falha documentados; *system prompt* aprovado pela equipe; dados simulados persistidos e lidos no SQLite. |
| **Sprint 2** | 30/11/2026 | 02/12/2026 | Medição precisa de latência (`time.perf_counter()`), contagem de tokens, controle de *rate limit* e criação/validação do banco de **300 perguntas** factuais curtas e inequívocas (CSV/JSON). | Dataset com 300 perguntas válidas contendo `id`, `pergunta`, `gabarito`, `sinonimos_aceitos`, `categoria` e `dificuldade`; cliente de API registra `latency_ms` e tokens com respeito ao RPM configurado sem estouro de cota. |
| **Sprint 3** | 07/12/2026 | 09/12/2026 | Persistência incremental no SQLite (`COMMIT` por requisição), execução da **coleta piloto** (20 a 30 perguntas reais) e implementação/validação do corretor automático (normalização + sinônimos). | Coleta piloto concluída com 20–30 registros reais salvos individualmente no SQLite; interrupção simulada não perde respostas já coletadas; corretor automático atinge ≥ 90% de concordância com conferência manual no piloto. |
| **Sprint 4** | 14/12/2026 | 16/12/2026 | Execução da **coleta completa** (300+ perguntas em lotes de 20 e horários variados), backup em CSV, correção automática total, **auditoria manual de 10%** e estatísticas descritivas + séries discretas. | Base completa (≥ 300 respostas por condição) coletada e exportada para backup CSV; 100% das respostas corrigidas automaticamente; amostra aleatória de 10% auditada manualmente com taxa de erro do corretor calculada; tabelas descritivas geradas. |
| **Sprint 5** | 21/12/2026 | 23/12/2026 | Modelagem estatística completa no Jupyter Notebook (Binomial em lotes de 20 com IC 95%, Geométrica/Binomial Negativa, Normal, Exponencial deslocada, Log-Normal), testes de aderência, superdispersão por dificuldade e apresentação final. | Notebook `notebooks/relatorio_final.ipynb` executado do início ao fim sem erros; QQ-plots, AIC/BIC, Qui-quadrado e KS gerados e exportados; análise de superdispersão por dificuldade concluída; slides/roteiro de apresentação final prontos. |

---

## Sequência de Dependências Críticas

1. **Sprint 1 → Sprint 2:** O contrato do schema SQLite e a interface da CLI precisam estar estáveis antes da carga das 300 perguntas e da instrumentação de métricas reais.
2. **Sprint 2 → Sprint 3:** O banco de 300 perguntas e o controle de *rate limit* são pré-requisitos para rodar a coleta piloto sem bloqueios de API.
3. **Sprint 3 → Sprint 4:** O corretor automático validado no piloto e o `COMMIT` por requisição garantem segurança para a coleta completa de 300+ perguntas.
4. **Sprint 4 → Sprint 5:** A base auditada (com viés do corretor medido) e o backup em CSV alimentam diretamente a modelagem probabilística final e os testes de aderência.
