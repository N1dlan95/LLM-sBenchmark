# Sprint 2 — Métricas Precisas, Rate Limit e Banco de 300 Perguntas

- **Alinhamento (Segunda):** 30/11/2026
- **Entrega (Quarta):** 02/12/2026
- **Critério de Aceite:** Dataset validado com 300 perguntas factuais curtas e inequívocas; cliente de API mede latência com `time.perf_counter()`, registra tokens e respeita *rate limit* sem erros 429.

---

## Tasks por Membro

### Membro 1 (Engenharia de Coleta & API)
- **[S2-T1]** Validar e padronizar a medição de latência em milissegundos usando exclusivamente `time.perf_counter()` ao redor da chamada de inferência nos providers (`gemini.py` e `openai_api.py`).
- **[S2-T2]** Garantir extração e normalização da contagem de tokens (`input_tokens`, `output_tokens` e total) retornados pelos SDKs, tratando casos em que metadados venham nulos.
- **[S2-T3]** Aprimorar o controle de *rate limit* (janela por RPM configurado) e *backoff* exponencial em `src/pipeline/runner.py`, registrando logs claros de espera e *retry* em caso de HTTP 429/5xx.

### Membro 2 (Curadoria & Auditoria de Dados)
- **[S2-T4]** Redigir e revisar o banco completo de **300 perguntas factuais curtas e inequívocas** (ex.: 100 fáceis, 100 médias, 100 difíceis; distribuídas entre categorias como Ciência, História, Geografia, Computação).
- **[S2-T5]** Preencher o campo `sinonimos_aceitos` para cada pergunta (ex.: variações numéricas, siglas, grafias equivalentes) visando reduzir falsos negativos do corretor automático.
- **[S2-T6]** Realizar revisão cruzada de ambiguidade nas 300 perguntas (eliminar perguntas dependentes de data corrente ou com múltiplas interpretações válidas).

### Membro 3 (Banco de Dados, Corretor & Testes)
- **[S2-T7]** Implementar script/função de importação e validação do arquivo de 300 perguntas (CSV/JSON) para a tabela `questions` do SQLite, checando unicidade de IDs, campos obrigatórios não nulos e distribuição por dificuldade.
- **[S2-T8]** Estender o schema/queries em `src/db.py` (se necessário) para armazenar `categoria`, `dificuldade` e `sinonimos_aceitos` de forma estruturada e consultável.
- **[S2-T9]** Escrever testes unitários validando o carregador de perguntas e o comportamento do *rate limiter* (usando relógio simulado ou intervalos curtos).

### Membro 4 (Modelagem Estatística & Visualização)
- **[S2-T10]** Implementar função exploratória para auditar o balanceamento do banco de 300 perguntas (contagem por `categoria` e `dificuldade`, comprimento dos prompts).
- **[S2-T11]** Preparar utilitários de extração de séries do SQLite para DataFrames/arrays (`pandas`/`numpy`) separando variáveis discretas (acertos/falhas) e contínuas (`latency_ms`, `output_tokens`).
