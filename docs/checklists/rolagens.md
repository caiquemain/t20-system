# 🎲 Sistema de Rolagens — Checklist

**Status:** ❌ Não iniciada
**Depende de:** nada (mas consome Engenhosidade/Desejos já implementados)

## Núcleo
- [ ] Componente de rolagem (1d20 + modificadores com tooltip da pilha)
- [ ] Botão de rolar em cada perícia (SkillList)
- [ ] Botão de rolar em cada ataque (AttackList: ataque + dano)
- [ ] Crítico/falha (nat 20 / nat 1) sinalizados visualmente
- [ ] Histórico de rolagens por ficha (persistido ou em sessão)

## Integrações com regras já existentes
- [ ] Engenhosidade (Kliren): consumir 2 PM automaticamente ao rolar perícia ativa
- [ ] Desejos (Qareen): aplicar -1 PM no custo ao lançar magia desejada
- [ ] CD de magias vs. Teste de Resistência do alvo
- [ ] Sorte (Hynne): motor de reroll integrado às rolagens
- [ ] Penalidade de armadura refletida nas rolagens de FOR/DES

## UX
- [ ] Modal/toast com resultado animado do dado
- [ ] Atalho de teclado para rolar perícia focada
- [ ] Exportar histórico de rolagens junto com o PDF (opcional)
