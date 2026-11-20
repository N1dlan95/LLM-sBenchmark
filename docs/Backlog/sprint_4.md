# Sprint 4 — Coleta Completa, Backup, Auditoria de 10% e Estatísticas Descritivas

- **Alinhamento (Segunda):** 14/12/2026
- **Entrega (Quarta):** 16/12/2026
- **Critério de Aceite:** Coleta completa (300+ perguntas em lotes de 20 e horários variados) finalizada e com backup em CSV; 100% corrigida automaticamente; amostra aleatória de 10% auditada manualmente com estimativa do viés do corretor; estatísticas descritivas e séries discretas calculadas.

---

## Tasks por Membro

### Membro 1 (Engenharia de Coleta & API)
- **[S4-T1]** Executar a **coleta completa** (300+ perguntas) organizada em lotes de 20, distribuída em horários variados do dia para capturar variações reais de latência e carga da API.
- **[S4-T2]** Monitorar logs de execução, *rate limits* e eventuais *retries* durante a coleta completa, garantindo integridade de todos os lotes no SQLite.
- **[S4-T3]** Implementar e executar rotina de **backup automático em CSV** exportando as tabelas consolidadas (`runs`, `questions`, `responses`, `grades`) para `data/backups/`.

### Membro 2 (Curadoria & Auditoria de Dados)
- **[S4-T4]** Sortear (com semente fixa para reprodutibilidade) uma **amostra aleatória estratificada de 10%** das respostas coletadas e realizar a **revisão manual completa**.
- **[S4-T5]** Registrar os resultados da auditoria manual no SQLite (`evaluation_method = 'manual'`) e documentar casos limítrofes e limitações observadas do experimento.

### Membro 3 (Banco de Dados, Corretor & Testes)
- **[S4-T6]** Executar o corretor automático em 100% da base coletada (`python app.py corrigir`).
- **[S4-T7]** Calcular o **viés e a acurácia do corretor automático** comparando as notas automáticas com a auditoria manual dos 10% (taxa de falso positivo, falso negativo e coeficiente de concordância Kappa/acurácia).
- **[S4-T8]** Verificar integridade referencial e ausência de valores ausentes/duplicados no SQLite e no backup CSV antes da modelagem final.

### Membro 4 (Modelagem Estatística & Visualização)
- **[S4-T9]** Calcular todas as **estatísticas descritivas** da base completa (média, mediana, variância, desvio padrão, IQR, assimetria e curtose para latência e tokens; proporção global e por categoria/dificuldade para acertos e falhas).
- **[S4-T10]** Construir as **séries discretas** necessárias para a Sprint 5: contagem de falhas por lote de 20 ($X_i$), número de tentativas até a 1ª falha (Geométrica) e até a $r$-ésima falha (Binomial Negativa), salvando tabelas resumo.
