# 📜 Origens do Livro Básico (T20 JdA) — Revisão & Cobertura

**Status:** ✅ 35/35 origens revisadas contra o Livro Básico (100% Concluída!)  
**Fontes de dados:** `app/src/dados_origens.py` e `app/src/dados_poderes_origem.py`  
**Cobertura:** 35/35 origens auditadas, 35/35 poderes exclusivos com `efeitos` declarativos, suíte `app/tests/test_origens.py` (`819 testes passando`)  
**Atualizado em:** 2026-11-26

---

## 📋 Checklist das 35 Origens (ordem alfabética)

- [x] **Acólito** (*Membro da Igreja*)
- [x] **Amigo dos Animais** (*Amigo Especial* — corrigido `pericias_fixas` indevidas + bônus de parceiro)
- [x] **Amnésico** (*Lembranças Graduais* concedido automaticamente pelo motor)
- [x] **Aristocrata** (*Sangue Azul*)
- [x] **Artesão** (*Frutos do Trabalho* — corrigido patamar *campeão*)
- [x] **Artista** (*Dom Artístico*)
- [x] **Assistente de Laboratório** (*Esse Cheiro...* — corrigido `pericias_fixas` + `Ofício (alquimista)`)
- [x] **Batedor** (*À Prova de Tudo*)
- [x] **Capanga** (*Confissão* — corrigido tempo para 1 minuto)
- [x] **Charlatão** (*Alpinista Social*)
- [x] **Circense** (*Truque de Mágica*)
- [x] **Criminoso** (*Punguista*)
- [x] **Curandeiro** (*Médico de Campo*)
- [x] **Eremita** (*Busca Interior*)
- [x] **Escravo** (*Desejo de Liberdade*)
- [x] **Estudioso** (*Palpite Fundamentado*)
- [x] **Fazendeiro** (*Água no Feijão* — `Ofício (fazendeiro)`)
- [x] **Forasteiro** (*Cultura Exótica*)
- [x] **Gladiador** (*Pão e Circo*)
- [x] **Guarda** (*Detetive*)
- [x] **Herdeiro** (*Herança*)
- [x] **Herói Camponês** (*Coração Heroico* — `+3/+6/+9/+12 PM` por patamar conectado ao motor)
- [x] **Marujo** (*Passagem de Navio*)
- [x] **Mateiro** (*Vendedor de Carcaças*)
- [x] **Membro de Guilda** (*Rede de Contatos* — corrigido tempo para 1 minuto)
- [x] **Mercador** (*Negociação*)
- [x] **Minerador** (*Escavador* — corrigido `pericias_fixas`, `Ofício (minerador)`, proficiência e `+1` dano com picareta)
- [x] **Nômade** (*Mochileiro* — `+5` espaços em `carga_maxima` conectado em `sincronizar_carga`)
- [x] **Pivete** (*Quebra-Galho* — corrigida divergência de capitalização com `beneficios_lista`)
- [x] **Refugiado** (*Estoico*)
- [x] **Seguidor** (*Antigo Mestre*)
- [x] **Selvagem** (*Vida Rústica* — imunidade a itens ingeríveis prejudiciais em `status.imunidades`)
- [x] **Soldado** (*Influência Militar*)
- [x] **Taverneiro** (*Gororoba* — `Ofício (cozinheiro)`)
- [x] **Trabalhador** (*Esforçado*)

---

## ✅ Critério de Pronto (atendido)
1. Conferência fiel contra o texto oficial do Livro Básico (T20 JdA p.85–95).
2. Efeitos declarativos modelados em 35/35 poderes de `dados_poderes_origem.py` e conectados ao motor (`status.py`, `inventario.py`, `habilidades.py`, `pericias.py`).
3. Suíte `app/tests/test_origens.py` validando catálogo, nomes, regras especiais e bônus mecânicos sem regressões.
