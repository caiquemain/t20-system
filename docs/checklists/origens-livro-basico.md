# 📜 Origens do Livro Básico (T20 JdA) — Revisão & Cobertura

**Status:** 🟡 0/35 origens revisadas contra o Livro Básico  
**Fontes de dados:** `app/src/dados_origens.py` e `app/src/dados_poderes_origem.py`  
**Estado atual:** 35 origens e 35 poderes exclusivos cadastrados (`9/35` com `efeitos`; `0` testes dedicados)  
**Atualizado em:** 2026-11-26

---

## 📋 Checklist das 35 Origens (ordem alfabética)

- [ ] **Acólito**
- [ ] **Amigo dos Animais**
- [ ] **Amnésico**
- [ ] **Aristocrata**
- [ ] **Artesão**
- [ ] **Artista**
- [ ] **Assistente de Laboratório**
- [ ] **Batedor**
- [ ] **Capanga**
- [ ] **Charlatão**
- [ ] **Circense**
- [ ] **Criminoso**
- [ ] **Curandeiro**
- [ ] **Eremita**
- [ ] **Escravo**
- [ ] **Estudioso**
- [ ] **Fazendeiro**
- [ ] **Forasteiro**
- [ ] **Gladiador**
- [ ] **Guarda**
- [ ] **Herdeiro**
- [ ] **Herói Camponês**
- [ ] **Marujo**
- [ ] **Mateiro**
- [ ] **Membro de Guilda**
- [ ] **Mercador**
- [ ] **Minerador**
- [ ] **Nômade**
- [ ] **Pivete**
- [ ] **Refugiado**
- [ ] **Seguidor**
- [ ] **Selvagem**
- [ ] **Soldado**
- [ ] **Taverneiro**
- [ ] **Trabalhador**

---

## ✅ Critério de Pronto (por origem)
1. Conferência fiel contra o texto oficial do Livro Básico (T20 JdA): itens iniciais, lista de perícias, lista de poderes e poder exclusivo de origem.
2. Efeitos mecânicos declarativos modelados em `dados_poderes_origem.py` e conectados ao motor (`app/src/regras/`).
3. Fluxo de escolha de benefícios de origem (2 benefícios, regra especial de *Amnésico*, itens iniciais, bônus de perícias/status) validado por suíte `app/tests/test_origens*.py`.
