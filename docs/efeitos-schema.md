# Schema de efeitos declarativos (motor T20)

Toda habilidade/poder tem `efeitos: dict[str, Any]`. **O motor consome
algumas chaves hoje; outras são declarativas** — ficam armazenadas
esperando o dia em que um VTT / mod (BG3, Foundry, etc.) precise delas.

## Chaves ATIVAS (motor lê hoje)

| Chave | Tipo | Semântica |
|---|---|---|
| `pv_max_ini`, `pv_max_nivel` | int | PV por nível inicial/total |
| `pm_max_nivel`, `pm_por_nivel_impar` | int | PM por nível |
| `deslocamento` | int | deslocamento base (m) |
| `defesa_bonus` | int | +Defesa |
| `ataque_extra_pm` | int | custo do ataque extra (arma natural) |
| `arma_natural` | str/dict | define um Ataque racial |
| `visao_escuro`, `visao_penumbra`, `faro` | bool | sentidos |
| `imunidade` | list | imunidades |
| `resistencia_rd`, `resistencia_rd_escolha` | dict/int | RD |
| `tipo_criatura` | str | substitui tipo (Monstro/Construto/etc) |
| `bonus_pericia`, `bonus_pericia_condicional` | dict | bônus de perícia |
| `pericia_atributo_opcao` | dict[str,str] | permite trocar atributo-chave |
| `pericia_escolha`, `pericia_bonus_escolha` | int/dict | slots de escolha |
| `pericia_treino` | list[str] | perícias treinadas à força (padrão motor) |
| `habilita_magia` | dict | habilita lançar magias |
| `magia_adicional`, `magia_adicional_escolha` | dict | magias concedidas |
| `reducao_custo_magia` | dict | -N PM em magias nomeadas |
| `reducao_custo_se_conhecida` | int | -N PM se reaprender |
| `reducao_custo_magia_global` | float | multiplicador global (Alta Arcana) |
| `reducao_pm_tipo` | dict | -N PM por tipo de dano |
| `cd_por_escola`, `custo_por_escola` | dict | bônus por escola |
| `cd_magia_bonus`, `cd_escola_bonus` | int | +CD de magia |
| `bonus_dano_magias`, `bonus_dano_dado_tipo` | int/dict | +dano em magias |
| `habilidade_ativavel` | dict | botão ativável (custo, ação, efeito) |
| `escolha_subclasse` | list | opções de caminho |

## Chaves DECLARATIVAS (motor ignora; VTT/mod lê)

| Chave | Tipo | Semântica |
|---|---|---|
| `contramagica_como_reacao` | bool | permite contramágica por reação |
| `sustentados_simultaneos` | int | máx. de efeitos sustentados |
| `sobrevive_a_dano_letal` | dict | reação a dano (ex.: Foco Vital) |
| `aprender_magias_por_copia` | dict | Escriba Arcano |
| `fabricar_pergaminho` | bool | Tinta do Mago |
| `fabricar_pocao` | bool | Caldeirão do Bruxo |
| `dano_explosao` | dict | Presas Afiadas (relança máximos) |
| `raio_elemental`, `raio_poderoso` | bool | flags de Raio Arcano |
| `heranca_nivel` | str | "aprimorada" / "superior" |
| `magias_extras` | int | +N magias (Conhecimento Mágico) |
| `aumento_atributo` | int | +N no atributo |
| `atributo_escolha` | int | slots de escolha de atributo |
| `familiar_escolha` | int | slots de escolha de familiar |
| `escola_escolha`, `escola_escolha` | int | slots de escola |
| `concentracao_dupla` | bool | reservado |

## Regras

1. Chaves em **snake_case**.
2. Valores sempre tipados (int/str/bool/list/dict) — nunca `None` solto.
3. Efeitos **aditivos**; o motor soma cada chave conforme o contexto.
4. Efeitos de **slots** (`_escolha`) só se ativam via `escolhas_aplicadas`.
5. Sempre que possível, documentar o gatilho (`gatilho: str`) para VTTs.

## Convenção de nomes para "vazio preparado"

Quando um poder tem efeito que o motor ainda não consome, ele **preenche
a chave declarativa + uma `nota` explicativa**. Exemplo:

```python
"efeitos": {
    "contramagica_como_reacao": True,
    "gatilho": "inimigo_lanca_magia",
    "custo_acao": "reacao",
    "nota": "Acao de combate nao modelada pelo motor; ver Lote 5 Arcanista.",
}
