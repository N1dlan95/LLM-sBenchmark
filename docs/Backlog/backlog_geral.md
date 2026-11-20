# Backlog Geral — Modelagem Probabilística da Alucinação e da Incerteza em LLMs

Este documento consolida os papéis da equipe e o índice das Sprints semanais (23/11/2026 a 23/12/2026).

---

## Divisão da Equipe (4 Membros)

| Papel | Responsabilidades Principais | Principais Arquivos no Repositório |
| :--- | :--- | :--- |
| **Membro 1 — Engenharia de Coleta & API** | Integração com SDK da LLM, CLI (`app.py`), controle de *rate limit* e medição de latência/tokens. | `app.py`, `src/providers/`, `src/pipeline/runner.py`, `.env.example` |
| **Membro 2 — Curadoria & Auditoria de Dados** | Redação do banco de 300 perguntas, definição do *system prompt*, revisão manual de 10% e documentação de limitações. | `config/experiment.yaml`, `data/questions.*`, `docs/` |
| **Membro 3 — Banco de Dados, Corretor & Testes** | Schema SQLite, gerador de dados simulados, corretor automático (`grader.py` / `src/pipeline/evaluator.py`) e testes de aderência/pressupostos. | `src/db.py`, `src/pipeline/evaluator.py`, `src/analytics/validation.py` |
| **Membro 4 — Modelagem Estatística & Visualização** | Distribuições discretas e contínuas (`stats_models.py` / `src/analytics/`), Jupyter Notebook e exportação dos gráficos finais. | `src/analytics/discrete.py`, `src/analytics/continuous.py`, `notebooks/relatorio_final.ipynb` |

---

## Índice do Backlog por Sprint

- [Sprint 1 (Entrega: 25/11/2026)](./sprint_1.md) — Setup, CLI, regra de falha, *system prompt*, `.env` e pipeline simulado.
- [Sprint 2 (Entrega: 02/12/2026)](./sprint_2.md) — Latência precisa, tokens, *rate limit* e banco de 300 perguntas factuais.
- [Sprint 3 (Entrega: 09/12/2026)](./sprint_3.md) — Persistência incremental (`COMMIT` por requisição), coleta piloto e corretor automático.
- [Sprint 4 (Entrega: 16/12/2026)](./sprint_4.md) — Coleta completa (300+ perguntas em lotes de 20), backup CSV, auditoria de 10% e estatísticas descritivas.
- [Sprint 5 (Entrega: 23/12/2026)](./sprint_5.md) — Modelagem estatística completa, testes de aderência, superdispersão e apresentação final.
