# Sprint 1 — Setup, CLI, Regra Operacional e Pipeline Simulado

- **Alinhamento (Segunda):** 23/11/2026
- **Entrega (Quarta):** 25/11/2026
- **Critério de Aceite:** CLI executa `coletar`, `corrigir` e `analisar` sem erros com dados simulados persistidos no SQLite; regra binária (`1 = acerto`, `0 = falha`) e *system prompt* curto formalizados.

---

## Tasks por Membro

### Membro 1 (Engenharia de Coleta & API)
- **[S1-T1]** Refatorar/estender a CLI em `app.py` com `argparse` expondo os subcomandos `coletar`, `corrigir` e `analisar` (além dos parâmetros `--config`, `--mock` e `--limit`).
- **[S1-T2]** Configurar carregamento seguro de variáveis de ambiente (`python-dotenv`) e criar `.env.example` com placeholders de chaves (`GEMINI_API_KEY`, `OPENAI_API_KEY`) sem expor segredos no Git.
- **[S1-T3]** Integrar a chamada de um provedor simulado (*mock*) na interface `LLMProvider` para permitir validação do fluxo de coleta sem consumo de cota real.

### Membro 2 (Curadoria & Auditoria de Dados)
- **[S1-T4]** Redigir e documentar a definição operacional da variável aleatória binária (`1 = acerto`, `0 = falha/alucinação`), incluindo critérios para respostas evasivas ou parcialmente corretas.
- **[S1-T5]** Definir e versionar em `config/experiment.yaml` o *system prompt* curto e padronizado (ex.: exigir resposta direta em no máximo 1 frase/termo) para estabilizar a variância de tokens de saída.
- **[S1-T6]** Criar um mini-lote inicial de 10 perguntas factuais de teste para validar o formato de entrada (CSV/JSON) com campos `id`, `categoria`, `dificuldade`, `pergunta`, `gabarito` e `sinonimos_aceitos`.

### Membro 3 (Banco de Dados, Corretor & Testes)
- **[S1-T7]** Revisar e validar o schema SQLite em `src/db.py` (`runs`, `questions`, `responses`, `grades`), garantindo compatibilidade com a regra `1 = acerto`, `0 = falha` e campos de metadados.
- **[S1-T8]** Implementar gerador de dados simulados (*mock dataset* com ~40 respostas Bernoulli sintéticas, latências e tokens) para testar inserção, leitura e correção ponta a ponta.
- **[S1-T9]** Criar teste de fumaça (*smoke test*) automatizado validando a execução sequencial `coletar --mock` → `corrigir` → `analisar` sobre o banco de testes.

### Membro 4 (Modelagem Estatística & Visualização)
- **[S1-T10]** Estruturar o subcomando `analisar` conectando as consultas SQLite aos módulos de `src/analytics/` para gerar um resumo inicial (taxa empírica $\hat{p}$, média e desvio padrão de latência/tokens) nos dados simulados.
- **[S1-T11]** Criar o esqueleto inicial do notebook `notebooks/relatorio_final.ipynb` com seções padronizadas (Introdução, Metodologia, Análise Exploratória, Modelos Discretos, Modelos Contínuos, Aderência e Conclusões).
