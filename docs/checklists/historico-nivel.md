# 📜 Histórico da Ficha ("git da ficha") — Checklist

**Status:** 🚧 Em andamento (MVP backend)
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
- [ ] Botão "⬆️ Subir de Nível" no header (substituir input NV? decidir)
- [ ] LevelUpModal passo 1: mostrar resumo de ganhos (só leitura)
- [ ] LevelUpModal passos de escolhas (poder/magia/perícia)
- [ ] Aba/painel "📜 Histórico": linha do tempo clicável
- [ ] Ver snapshot de um evento (ficha read-only naquele nível)
- [ ] Botão "Restaurar" (grava evento de restauração, não apaga nada)

## Regras de ouro
- Histórico é append-only: NUNCA deletar ou reescrever eventos
- Restaurar = criar evento novo apontando para o snapshot antigo
- Snapshot guarda a ficha COMPLETA (time machine barata em Mongo)
