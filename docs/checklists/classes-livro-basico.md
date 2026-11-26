# ⚔️ Classes do Livro Básico (T20 JdA) — Cobertura

**Status:** 🟡 13/14 classes completas (falta apenas Paladino)  
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
| **Cavaleiro** | 26 (6 fixas + 20 poderes) | 26 (100%) | 2 arquivos (`test_cavaleiro_*`) | ✅ Completa |
| **Clérigo** | 21 (3 fixas + 18 poderes) | 21 (100%) | 2 arquivos (`test_clerigo_*`) | ✅ Completa |
| **Druida** | 27 (5 fixas + 22 poderes) | 27 (100%) | 2 arquivos (`test_druida_*`) | ✅ Completa |
| **Guerreiro** | 23 (4 fixas + 19 poderes) | 23 (100%) | 2 arquivos (`test_guerreiro_*`) | ✅ Completa |
| **Inventor** | 38 (8 fixas + 30 poderes) | 38 (100%) | 2 arquivos (`test_inventor_*`) | ✅ Completa |
| **Ladino** | 27 (7 fixas + 20 poderes) | 27 (100%) | 2 arquivos (`test_ladino_*`) | ✅ Completa |
| **Lutador** | 29 (6 fixas + 23 poderes) | 29 (100%) | 2 arquivos (`test_lutador_*`) | ✅ Completa |
| **Nobre** | 26 (8 fixas + 18 poderes) | 26 (100%) | 2 arquivos (`test_nobre_*`) | ✅ Completa |
| **Paladino** | 11 (6 fixas + 5 poderes) | 3 (27%) | — | 🟡 Parcial |

---

## 📋 Lotes de Execução

### Lote 1 — Marciais
- [x] **Guerreiro** (Ataque Especial, Durão, Ataque Extra, Campeão + 19 poderes + testes)
- [x] **Lutador** (Briga, Golpe Relâmpago, Casca Grossa, Golpe Cruel, Golpe Violento, Dono da Rua + 23 poderes + testes)
- [x] **Cavaleiro** (Código de Honra, Baluarte, Duelo, Caminho do Cavaleiro, Resoluto, Bravura Final + 20 poderes + testes)

### Lote 2 — Especialistas
- [x] **Ladino** (Ataque Furtivo, Especialista, Evasão, Esquiva Sobrenatural, Olhos nas Costas, Evasão Aprimorada, A Pessoa Certa para o Trabalho + 20 poderes + testes)
- [x] **Caçador** (Marca da Presa, Rastreador, Explorador, Caminho do Explorador, Mestre Caçador + 23 poderes + testes)
- [x] **Bucaneiro** (Audácia, Insolência, Evasão, Esquiva Sagaz, Panache, Evasão Aprimorada, Sorte de Nimb + 19 poderes + testes)

### Lote 3 — Divinos & Suporte
- [x] **Clérigo** (Devoto Fiel, Magias, Mão da Divindade + 18 poderes + testes)
- [ ] **Paladino** (Abençoado, Golpe Divino, Cura pelas Mãos, Aura Sagrada + poderes + testes)
- [x] **Druida** (Devoto Fiel, Empatia Selvagem, Magias, Caminho dos Ermos, Força da Natureza + 22 poderes + testes)

### Lote 4 — Versáteis & Complexas
- [x] **Bardo** (Inspiração, Magias, Eclético, Artista Completo + 20 poderes + testes)
- [x] **Nobre** (Autoconfiança, Espólio, Orgulho, Palavras Afiadas, Riqueza, Gritar Ordens, Presença Aristocrática, Realeza + 18 poderes + testes)
- [x] **Inventor** (Engenhosidade, Protótipo, Fabricar Item Superior/Mágico, Comerciante, Encontrar Fraqueza, Olho do Dragão, Obra-Prima + 30 poderes + testes)

## ✅ Critério de Pronto (por classe)
- Catálogo completo de habilidades fixas (nv 1–20) e poderes do Livro Básico
- Efeitos declarativos conectados ao motor (`app/src/regras/`)
- Suíte `test_<classe>_*.py` passando sem regressões
