# Checklist de Alinhamento Semanal (10 Minutos)

**Quando:** Toda segunda-feira, durante o horário da aula (**23/11, 30/11, 07/12, 14/12 e 21/12/2026**).  
**Objetivo:** Revisar o progresso, destravar impedimentos técnicos e validar o escopo da entrega de quarta-feira.

---

## Roteiro Cronometrado (10 min)

### 1. Status Rápido por Membro (0:00 – 03:00 | ~45s por pessoa)
Cada integrante responde objetivamente apenas 3 perguntas:
- [ ] O que foi concluído desde a última quarta-feira?
- [ ] Qual task está em andamento hoje para a entrega desta quarta?
- [ ] Existe algum bloqueio técnico (API, dataset, SQLite, biblioteca)?

### 2. Verificação de Contrato & Integração (03:00 – 06:00)
- [ ] **Schema / Dados:** As colunas do SQLite (`runs`, `questions`, `responses`, `grades`) e formatos de CSV/JSON estão compatíveis entre coleta, corretor e análise?
- [ ] **Branch / Git:** Todos os códigos recentes estão commitados e testáveis na `main` (ou branch de integração) sem conflitos?
- [ ] **Reprodutibilidade:** As variáveis de ambiente (`.env`) e dependências (`requirements.txt`) estão atualizadas?

### 3. Check Específico da Sprint da Semana (06:00 – 08:30)
- **23/11 (Sprint 1):** Regra binária (`1 = acerto`, `0 = falha`) e *system prompt* curto fechados? Pipeline simulado roda ponta a ponta?
- **30/11 (Sprint 2):** As 300 perguntas têm gabarito inequívoco e sinônimos? `perf_counter()` e *rate limit* testados sem erro 429?
- **07/12 (Sprint 3):** `COMMIT` por requisição confirmado? Coleta piloto (20–30 perguntas) agendada e corretor validado?
- **14/12 (Sprint 4):** Coleta completa (lotes de 20 em horários variados) com backup CSV garantido? Amostra de 10% sorteada para auditoria?
- **21/12 (Sprint 5):** Todos os testes de aderência (KS, Qui-quadrado, QQ-plot, AIC/BIC) rodando no notebook? Gráficos exportados e divisão da fala da apresentação definida?

### 4. Decisões e Plano de Ação até Quarta-feira (08:30 – 10:00)
- [ ] Registrar responsáveis e prazos para qualquer impedimento identificado.
- [ ] Confirmar horário de *freeze* do código na terça-feira à noite para evitar quebras na entrega de quarta.
- [ ] Validar quem fará o upload/demonstração da entrega da quarta-feira.
