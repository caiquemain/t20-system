# 📄 PDF da Ficha — Checklist de Melhorias

**Status:** ✅ MVP funcional (entregue em 17/set/2026)
**Endpoint:** `GET /personagens/{id}/pdf` (app/src/routers/pdf.py)
**Template:** `app/assets/ficha-t20-template.pdf`
**Foco atual:** NENHUM — ferramenta minimamente funcional, refinar só depois

## 🎯 Mapeamento de campos pendentes
- [ ] Modificadores de atributos (ModFor, ModDes, ModCon, ModInt, ModSab, ModCar)
- [ ] Ofícios com nome customizado (campos `Ofício 1` / `Ofício_2` + totais 233/243)
- [ ] Checkboxes de treino (`Mar Trei acro`, `Mar Trei ades`, ...)
- [ ] Colunas 1/2, Atr, Tr, Out das perícias (hoje só preenche o Total)
- [ ] Atributo-chave de magias (`SeleAtribMagia` / `ModAtribMagia`)
- [ ] Teste de Resistência (`TesteResist`)
- [ ] Defesa detalhada (Base CA, B.Arm, B.Esc, Outros B.CA)
- [ ] Armadura & Escudo (Armadura, Escudo, Pa, Pe, PArmTotal)
- [ ] Proficiências (campo `Proficiências`)
- [ ] Dinheiro (T$, TO, TL/TP)
- [ ] Tamanho (`SeleTamanho`, ModFurtTam, ModManTam)
- [ ] Levantar (10x For) e nota de sobrecarga

## 🧠 Lógica
- [ ] Multiclasse no campo CLASSE (hoje só a 1ª classe)
- [ ] Quebra de linha / truncamento em Habilidades, Magias e Anotações
- [ ] Sanitizar nome do arquivo (acentos/espaços no nome do personagem)
- [ ] PVs/PMs Atuais: decidir se preenche ou mantém em branco (hoje: em branco)

## 🚀 Performance & Robustez
- [ ] Cache do template em memória (evita ler 4.6MB por request)
- [ ] Validação do template no startup (fail fast)
- [ ] Testes automatizados do endpoint (tests/test_pdf.py)
- [ ] Log de campos preenchidos vs. ignorados (debug de mapeamento)

## 🎨 UX
- [ ] Estado de loading no botão durante a geração
- [ ] Data de geração no rodapé
- [ ] Watermark discreto "Gerado por T20 System"
- [ ] Suporte a múltiplos templates (simples/completo)
