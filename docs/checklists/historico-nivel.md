# 📜 Histórico da Ficha ("git da ficha") — Checklist

**Status:** ✅ MVP completo (backend + frontend) — refinamentos na fila
**Conceito:** eventos append-only + snapshot por nível = memória do personagem
**Decisão de design:** resumo de level-up vem do DIFF antes/depois do
`atualizar_ficha()` — a memória nunca mente, pois nasce do motor de regras.

## Backend (MVP)
- [x] Modelo `EventoFicha` em models.py
- [x] `regras/historico.py`: `resumir_mudancas(antes, depois)`
- [x] Router `historico.py`: level-up, listar, ver evento, restaurar
- [x] Router registrado no main.py
- [x] Testes unitários do diff
- [ ] Índice na coleção `historico` (personagem_id + criado_em)
- [ ] Evento "criacao" gravado ao criar ficha nova (POST /personagens)

## Backend (escolhas no level-up)
- [ ] Body do level-up aceitar escolhas (poder, magia, perícia treinada)
- [ ] Validar escolhas contra requisitos (reutilizar validators)
- [ ] Bloquear level-up com escolhas pendentes obrigatórias

## Frontend
- [x] Botão "⬆️ Level Up" no header (coexiste com input NV — decisão de design)
- [ ] LevelUpModal passo 1: mostrar resumo de ganhos (só leitura)
- [ ] LevelUpModal passos de escolhas (poder/magia/perícia)
- [x] Aba "📜 HISTÓRICO": linha do tempo com cards roxos/laranja
- [ ] Ver snapshot de um evento (ficha read-only naquele nível)
- [x] Botão "⏪ Restaurar" por evento (append-only, nunca apaga)

## Regras de ouro
- Histórico é append-only: NUNCA deletar ou reescrever eventos
- Restaurar = criar evento novo apontando para o snapshot antigo
- Snapshot guarda a ficha COMPLETA (time machine barata em Mongo)
