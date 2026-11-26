# ⚔️ Classes do Livro Básico (T20 JdA) — Cobertura

**Status:** 🟡 5/14 classes completas (Arcanista, Bárbaro, Bardo, Bucaneiro e Caçador)  
**Fonte de dados:** `app/src/dados_habilidades_classe.py`  
**Atualizado em:** 2026-11-26

---

## 📊 Panorama Atual

| Classe | Entradas cadastradas | Com `efeitos` | Testes dedicados | Status |
|---|---|---|---|---|
| **Arcanista** | 24 (3 fixas + 21 poderes) | 24 (100%) | 6 arquivos (`test_arcanista_*`, `test_poderes_arcanista.py`) | ✅ Completa |
| **Bárbaro** | 24 (4 fixas + 20 poderes) | 24 (100%) | 5 arquivos (`test_barbaro_*`) | ✅ Completa |
| **Bardo** | 24 (4 fixas + 20 poderes) | 24 (100%) | 3 arquivos (`test_bardo_*`) | ✅ Completa |
| **Bucaneiro** | 26 (7 fixas + 19 poderes) | 26 (100%) | 2 arquivos (`test_bucaneiro_*`) | ✅ Completa |
| **Caçador** | 28 (5 fixas + 23 poderes) | 28 (100%) | 2 arquivos (`test_cacador_*`) | ✅ Completa |
| **Druida** | 10 (4 fixas + 6 poderes) | 9 (90%) | — | 🟡 Parcial |
| **Ladino** | 11 (4 fixas + 7 poderes) | 7 (64%) | — | 🟡 Parcial |
| **Inventor** | 8 (2 fixas + 6 poderes) | 5 (63%) | — | 🟡 Parcial |
| **Clérigo** | 8 (2 fixas + 6 poderes) | 3 (38%) | — | 🟡 Parcial |
| **Guerreiro** | 9 (3 fixas + 6 poderes) | 3 (33%) | — | 🟡 Parcial |
| **Lutador** | 9 (3 fixas + 6 poderes) | 3 (33%) | — | 🟡 Parcial |
| **Paladino** | 11 (6 fixas + 5 poderes) | 3 (27%) | — | 🟡 Parcial |
| **Nobre** | 9 (4 fixas + 5 poderes) | 2 (22%) | — | 🟡 Parcial |
| **Cavaleiro** | 9 (3 fixas + 6 poderes) | 1 (11%) | — | 🟡 Parcial |

---

## 📋 Lotes de Execução

### Lote 1 — Marciais
- [ ] **Guerreiro** (Ataque Especial, Durão, Golpe Pessoal + todos os poderes do JdA + testes)
- [ ] **Lutador** (Briga, Golpe Relâmpago, Casca Grossa + poderes + testes)
- [ ] **Cavaleiro** (Código de Honra, Baluarte, Duelo, Montaria + poderes + testes)

### Lote 2 — Especialistas
- [ ] **Ladino** (Ataque Furtivo, Especialista, Evasão + poderes + testes)
- [x] **Caçador** (Marca da Presa, Rastreador, Explorador, Caminho do Explorador, Mestre Caçador + 23 poderes + testes)
- [x] **Bucaneiro** (Audácia, Insolência, Evasão, Esquiva Sagaz, Panache, Evasão Aprimorada, Sorte de Nimb + 19 poderes + testes)

### Lote 3 — Divinos & Suporte
- [ ] **Clérigo** (Devoto Fiel, Magias Divinas, Canalizar Energia + poderes + testes)
- [ ] **Paladino** (Abençoado, Golpe Divino, Cura pelas Mãos, Aura Sagrada + poderes + testes)
- [ ] **Druida** (Devoto, Empatia Selvagem, Forma Selvagem, Magias + poderes + testes)

### Lote 4 — Versáteis & Complexas
- [x] **Bardo** (Inspiração, Magias, Eclético, Artista Completo + 20 poderes + testes)
- [ ] **Nobre** (Autoconfiança, Espólio, Orgulho, Gritar Ordens + poderes + testes)
- [ ] **Inventor** (Engenhosidade, Protótipo, Fabricar Item Superior, Engenhocas + poderes + testes)

## ✅ Critério de Pronto (por classe)
- Catálogo completo de habilidades fixas (nv 1–20) e poderes do Livro Básico
- Efeitos declarativos conectados ao motor (`app/src/regras/`)
- Suíte `test_<classe>_*.py` passando sem regressões
