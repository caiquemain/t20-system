# 🧬 Raças — Validação E2E — Checklist

**Status:** 🟡 Parcial — 14 de 17 raças do T20 JdA validadas
**Validadas:** Humano, Elfo, Anão, Goblin, Kliren, Qareen, Golem, Osteon,
Sereia/Tritão, Sílfide, Suraggel (ambas), Trog, Medusa, Lefou

## Pendentes
- [ ] Minotauro: chifres (ataque natural), +2 FOR +1 CON -1 SAB, tamanho Grande
- [ ] Dahllan: magias raciais, ataque natural, escolhas de atributos
- [ ] Hynne: Sorte (reroll — depende do sistema de rolagens), tamanho Pequeno, +2 DES +1 CAR -1 FOR

## Validação final das já prontas
- [ ] Lefou: Deformidade E2E (gravação atômica + 1 poder Tormenta) — reconfirmar após refactor
- [ ] Sereia: Canção dos Mares com blacklist entre slots — reconfirmar
- [ ] Golem: Propósito de Criação após migração de ficha antiga

## Limpeza técnica
- [ ] Remover logs temporários `[RACIAL-DEBUG]` de Ficha.tsx e useFicha.ts
- [ ] Remover sondas `[RACIAL][ROW]`/`[RENDER]` se ainda existirem
- [ ] Unificar RACAS_METADATA (Ficha.tsx) com dados_racas.py do backend (fim da duplicação)
