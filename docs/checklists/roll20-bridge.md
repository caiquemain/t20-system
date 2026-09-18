# 🌉 Ponte Roll20 — Checklist

**Status:** ❌ Feature futura (só checklist por hora — NÃO implementar ainda)
**Objetivo:** com 1 clique, a ficha inteira do nosso sistema vai para o Roll20;
depois, monstros/NPCs também entram na mesa com 1 clique.
**Navegador alvo:** Edge (Chromium) — navegador de testes do usuário.
Manifest V3 do Chrome carrega nativo no Edge; MESMO pacote serve os dois
(sem build separado, diferente do Firefox que exigiria manifest próprio).
**Inspiração:** github.com/pyanderson/roll20_tormenta20_grimoire
**Decisão:** template alvo = Tormenta20 Game of the Year (JdA) — versão mais recente

## 💡 Conceito (NÃO é import!)
A extensão do Roll20 não "importa" arquivo: ela injeta content scripts na
página e manipula o DOM da ficha. Nossa ponte faz o mesmo mecanismo, mas no
sentido inverso do repo de referência:
- Repo referência: enriquece a ficha burra do Roll20 (seletores, grimório)
- Nossa ponte: lê NOSSA ficha (motor de regras + histórico) e preenche o Roll20

Fluxo alvo:
1. Nosso app (localhost:5173) → botão "📤 Enviar pro Roll20"
2. Extensão lê o JSON da ficha (content script no nosso domínio)
3. JSON viaja via chrome.storage.local (ponte entre domínios)
4. Content script injetado em app.roll20.net preenche os campos da ficha

## Fase 1 — Export/Import JSON (sem extensão ainda)





## Fase 2 — Extensão Chromium (MV3, Edge primeiro)
- [x] Scaffold `t20-roll20-bridge/` (MV3, sem build: JS puro) (manifest.v3.json, popup, 2 content scripts)
- [x] `content-t20system.js`: botão flutuante lê a ficha via API
- [x] `content-roll20.js`: campos simples (Sessão 1) — repeating na Sessão 2


- [x] Inspecionar HTML da ficha no Roll20: mapa completo em `docs/roll20-field-mapping.md`
      (332+ campos extraídos, incluindo repeating sections e campos menace/NPC)
- [x] Template decidido: **Tormenta20 Game of the Year** (JdA, mais recente)
      → field-mapping.ts mapeia SOMENTE os campos desse template

- [x] Teste manual no Edge: NÍVEL/PV/PM ok, console limpo

## Fase 3 — Monstros & NPCs (depois da ponte de ficha)
- [ ] Bestiário no backend (dados próprios ou OGL — ver nota de licença)
- [ ] Injetar token + stats na mesa do Roll20 com 1 clique
- [ ] Lista rápida de NPCs favoritos do mestre

## ⚖️ Nota de licença
- Reusar dados do repo pyanderson (bestiário etc.) = conteúdo sob OPEN GAME
  LICENSE → trazer arquivo OPEN_GAME_LICENSE + créditos pro nosso repo
- Nossos `dados_*.py` são autoria própria: estamos limpos hoje

## 🔗 Sinergias com features existentes
- Export JSON = snapshot do histórico serializado (historico-nivel.md)
- Rolagens nativas (rolagens.md) podem virar macros de roll no Roll20 depois

## Sessão 2 — save via modelos internos (ENTREGUE)
- [x] Save persistente via `window.Campaign.characters.get(id).attribs` (attr.save/create)
- [x] Nome do personagem via `character.save({name})` (@{character_name} é referência reservada)
- [x] Repeating sections via atributos com UUID Roll20: ataques, habilidades,
      poderes, magias por círculo (repeating_spells1..5), equipamentos
- [x] Background executa o fill no MAIN world (chrome.scripting.executeScript)
- [x] Content script isolado só delega (storage pending + mensagens)
- [x] Validado no Edge: persiste após fechar/reabrir; workers recalculam
      defesa e totais de perícia a partir dos nossos atributos

## Pendências da ponte (futuro)

- [x] Dinheiro (attr_ts / attr_to): SINCRONIZADO — a ficha principal TEM campo
      Dinheiro (to/tl/tp). Mapeamento: tl→attr_ts (T$), to→attr_to (T. Ouro);
      cobre (tp) não tem campo na ficha JdA oficial — ignorado de propósito.
- [x] Condições ativas: DECIDIDO — jogador marca na mesa; Roll20 é a fonte
      durante a sessão. Ponte NÃO sincroniza condições.
- [ ] Modo "ficha nova": criar character no Roll20 direto da ponte
- [ ] Fase 3: monstros/NPCs (cstype=1 + campos attr_menace_*)

## Estado REAL da ponte (atualizado após Sessão 2b + dinheiro)

### ✅ Já entregue e funcionando (persiste no Roll20 via window.Campaign)
- [x] Scaffold MV3 + 2 content scripts + background service worker
- [x] Cabeçalho completo (nome, jogador, raça, origem, classe/nível, XP, divindade)
- [x] Nome do personagem via `character.save({name})` (referência reservada do Roll20)
- [x] 6 atributos (FOR/DES/CON/INT/SAB/CAR)
- [x] PV/PM máx+atuais, deslocamento, tamanho
- [x] Proficiências e anotações
- [x] Perícias: checkbox `_treinada` + select `atributo2` + diff em `outros`
  (coluna Outros = 0 confirma que motor e ficha JdA concordam na regra de treino)
- [x] Dinheiro: Tibar (tl→attr_ts) e T. Ouro (to→attr_to); cobre (tp) sem campo na JdA
- [x] Ataques (repeating_attacks) com crítico parseado (margem/multiplicador)
- [x] Habilidades gerais (repeating_abilities)
- [x] Poderes de classe (repeating_powers)
- [x] Magias por círculo (repeating_spells1..5)
- [x] Equipamentos (repeating_equipment) com quantidade e slots

### ⏳ Pendências REAIS da ponte
- [ ] **Modo "ficha nova"**: criar character no Roll20 direto da ponte (sem precisar criar no site primeiro)
- [ ] **Fase 3 — Monstros/NPCs** com 1 clique:
  - Botão separado no backend "monstros" com `cstype=1`
  - Mapa: `attr_menace_name`, `menace_nd`, `menace_hp`, `menace_mp`,
    `menace_for/des/con/int/sab/car`, `menace_desloc`, `menace_defense`,
    `menace_perception`, `menace_init`, `menace_fortitude`, `menace_reflex`,
    `menace_will`, `repeating_menaceabilities`, `repeating_menacespells`,
    `repeating_menacemelee`, `repeating_menacedistance`, `menace_treasure`,
    `menace_treasures`

### ❌ Cortado por decisão de escopo
- Condições ativas (attr_abalado etc.) — jogador marca na mesa; Roll20 é a fonte
- Dinheiro em cobre (tp) — ficha JdA oficial não tem campo
