# Scripts de desenvolvimento

Ferramentas one-shot para auditoria e diagnóstico. **Não são parte do
runtime da API.** Não importar de `src/`.

## audit_racas.py

Cria 1 ficha por raça (Guerreiro nv 1) e imprime o estado final:
atributos, tamanho, deslocamento, PV/PM, habilidades, efeitos ativos,
magias, Defesa, RD, imunidades, sentidos, vulnerabilidades, proficiências.

Rodar dentro do container:

    docker compose exec -T api python scripts/audit_racas.py
