# 📄 PDF da Ficha — Checklist de Melhorias

**Status:** ✅ Concluído com PyMuPDF + cache em memória + suíte automatizada (`app/tests/test_pdf.py`)  
**Endpoint:** `GET /personagens/{id}/pdf` (`app/src/routers/pdf.py`)  
**Template:** `app/assets/ficha-t20-template.pdf`  
**Atualizado em:** 2026-11-26

## ✅ Já entregue (rewrite PyMuPDF + Refinamento Completo)
- [x] Migração de `pypdf` para `pymupdf` (import moderno `import pymupdf`, sem warning de depreciação)
- [x] Cabeçalho (nome, jogador, raça, origem, multiclasse / subclasse em `CLASSE`, nível, divindade, XP)
- [x] Atributos (`For`..`Car`) e modificadores reais (`ModFor`..`ModCar`) preenchidos para todos os visualizadores de PDF
- [x] PVs/PMs Totais e Atuais (preservando valores atuais no recálculo), Deslocamento (`Xm`), CA detalhada (`Base CA`, `arm pesa`, `ModAtribDefe`, `B.Arm`, `B.Esc`, `Outros B.CA`)
- [x] Armadura & Escudo (`Armadura`, `B.Arm1`, `Pa`, `Escudo`, `B.Esc2`, `Pe`, `PArmTotal`)
- [x] Proficiências (`Proficiências`), Dinheiro (`T`, `TO`), Tamanho (`SeleTamanho`, `ModFurtTam`, `ModManTam`) e Carga/Levantar (`CargaTotal`, `CargaMax`, `Levantar`)
- [x] Todas as colunas das 30 perícias (`xx0` Total, `xx1` 1/2 Nível, `SeleAtrib*`, `ModAtrib*`, `xx3` Treino, `xx4` Outros, `Mar Trei *`) + Ofícios customizados (`Ofício 1` / `Ofício_2`)
- [x] Ataques (até 5), Equipamentos (até 15, com quantidade `(xN)`)
- [x] Página 2: Habilidades (Raça/Origem e Classe/Poderes), Atributo-chave (`SeleAtribMagia`/`ModAtribMagia`), CD (`TesteResist`), Magias com aprimoramentos, `Descrição` (Idade, Alinhamento, Aparência, Personalidade, História) e `Anotações` com data de geração (sem sobrescrever `Observação` da Página 1)
- [x] Sanitização do nome do arquivo no `Content-Disposition` (ASCII slug seguro)
- [x] Quebra/truncamento inteligente (`_truncar_texto`), cache do template em memória (`@lru_cache`) com validação fail-fast
- [x] Estado de loading no botão **Baixar PDF** (`Ficha.tsx`)
- [x] Testes automatizados completos (`app/tests/test_pdf.py`)
