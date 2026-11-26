# 📄 PDF da Ficha — Checklist de Melhorias

**Status:** 🟢 Funcional com PyMuPDF + suíte automatizada (`app/tests/test_pdf.py`)  
**Endpoint:** `GET /personagens/{id}/pdf` (`app/src/routers/pdf.py`)  
**Template:** `app/assets/ficha-t20-template.pdf`  
**Atualizado em:** 2026-11-25

## ✅ Já entregue (rewrite PyMuPDF + Bloco 1)
- [x] Migração de `pypdf` para `pymupdf` (import moderno `import pymupdf`, sem warning de depreciação)
- [x] Cabeçalho (nome, jogador, raça, origem, classe primária, nível, divindade)
- [x] Atributos convertidos para valor do template + PVs/PMs Totais e Atuais + CA + Deslocamento + XP
- [x] Checkboxes de treino (`Mar Trei acro`, `Mar Trei luta`, ...) + coluna Outros (`x4`)
- [x] Ataques (até 5), Equipamentos (até 15) + Carga Total/Máxima
- [x] Habilidades (Raça/Origem e Classe/Poderes) + Magias completas com aprimoramentos + Observações
- [x] Sanitização do nome do arquivo no `Content-Disposition` (ASCII slug seguro)
- [x] Testes automatizados (`app/tests/test_pdf.py`)

## 🎯 Mapeamento de campos pendentes
- [ ] Modificadores de atributos (`ModFor`, `ModDes`, `ModCon`, `ModInt`, `ModSab`, `ModCar`)
- [ ] Ofícios com nome customizado (`Ofício 1` / `Ofício_2` + totais `233`/`243`)
- [ ] Colunas 1/2, Atr, Tr das perícias (hoje preenche checkbox de treino + Outros)
- [ ] Atributo-chave de magias (`SeleAtribMagia` / `ModAtribMagia`) e CD (`TesteResist`)
- [ ] Defesa detalhada (Base CA, B.Arm, B.Esc, Outros B.CA)
- [ ] Armadura & Escudo (`Armadura`, `Escudo`, `Pa`, `Pe`, `PArmTotal`)
- [ ] Proficiências (`Proficiências`) e Dinheiro (`T$`, `TO`, `TL`/`TP`)
- [ ] Tamanho (`SeleTamanho`, `ModFurtTam`, `ModManTam`) e Levantar (10x For)

## 🧠 Lógica & Robustez
- [ ] Multiclasse no campo `CLASSE` (hoje só a 1ª classe)
- [ ] Quebra de linha / truncamento inteligente em Habilidades, Magias e Anotações
- [ ] Cache do template em memória (evita reler 4.6MB do disco por request)
- [ ] Validação do template no startup (fail fast)

## 🎨 UX
- [ ] Estado de loading no botão durante a geração
- [ ] Data de geração / watermark discreto no rodapé
