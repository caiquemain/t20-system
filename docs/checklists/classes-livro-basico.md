# ⚔️ Classes do Livro Básico (T20 JdA) — Cobertura

**Status:** 🟡 2/14 classes completas (Arcanista e Bárbaro)  
**Fonte de dados:** `app/src/dados_habilidades_classe.py`  
**Atualizado em:** 2026-11-25

---

## 📊 Panorama Atual

| Classe | Entradas cadastradas | Com `efeitos` | Testes dedicados | Status |
|---|---|---|---|---|
| **Arcanista** | 24 (3 fixas + 21 poderes) | 24 (100%) | 6 arquivos (`test_arcanista_*`, `test_poderes_arcanista.py`) | ✅ Completa |
| **Bárbaro** | 24 (4 fixas + 20 poderes) | 24 (100%) | 4 arquivos (`test_barbaro_*`) | ✅ Completa |
| **Druida** | 10 (4 fixas + 6 poderes) | 9 (90%) | — | 🟡 Parcial |
| **Caçador** | 9 (3 fixas + 6 poderes) | 6 (67%) | — | 🟡 Parcial |
| **Ladino** | 11 (4 fixas + 7 poderes) | 7 (64%) | — | 🟡 Parcial |
| **Inventor** | 8 (2 fixas + 6 poderes) | 5 (63%) | — | 🟡 Parcial |
| **Bucaneiro** | 11 (5 fixas + 6 poderes) | 5 (45%) | — | 🟡 Parcial |
| **Bardo** | 9 (3 fixas + 6 poderes) | 4 (44%) | — | 🟡 Parcial |
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
- [ ] **Caçador** (Marca da Presa, Rastreador, Explorador + poderes + testes)
- [ ] **Bucaneiro** (Audácia, Insolência, Evasão, Panache + poderes + testes)

### Lote 3 — Divinos & Suporte
- [ ] **Clérigo** (Devoto Fiel, Magias Divinas, Canalizar Energia + poderes + testes)
- [ ] **Paladino** (Abençoado, Golpe Divino, Cura pelas Mãos, Aura Sagrada + poderes + testes)
- [ ] **Druida** (Devoto, Empatia Selvagem, Forma Selvagem, Magias + poderes + testes)

### Lote 4 — Versáteis & Complexas
- [ ] **Bardo** (Inspiração, Magias, Eclético + poderes + testes)
- [ ] **Nobre** (Autoconfiança, Espólio, Orgulho, Gritar Ordens + poderes + testes)
- [ ] **Inventor** (Engenhosidade, Protótipo, Fabricar Item Superior, Engenhocas + poderes + testes)

## ✅ Critério de Pronto (por classe)
- Catálogo completo de habilidades fixas (nv 1–20) e poderes do Livro Básico
- Efeitos declarativos conectados ao motor (`app/src/regras/`)
- Suíte `test_<classe>_*.py` passando sem regressões
