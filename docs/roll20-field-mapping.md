# 🗺️ Roll20 Field Mapping — Tormenta20 JdA (Game of the Year)

**Fonte:** inspeção do DOM da ficha oficial JdA no Roll20 (HTML colado em 18/set/2026)
**Confirmação de template:** `attr_game_system = "tormenta20jda"` ✅
**Uso:** referência para o `field-mapping.ts` da ponte (docs/checklists/roll20-bridge.md)

## ⚠️ Regras de ouro da ficha JdA
1. **Totais são calculados por workers** (inputs disabled com data-formula).
   NUNCA escrever em: `attr_<pericia>total`, `attr_defesatotal`, `attr_cdtotal`,
   `attr_<pericia>treino`, `attr_carga`, `attr_limite`, `attr_maxima`.
   Escrever nos editáveis e deixar o worker recalcular.
2. **Repeating sections** criam linhas com ID gerado:
   `repeating_<grupo>_<ROWID>_<campo>`. A ponte precisa criar a linha
   (setAttrs com ID novo ou clique no +Add).
3. **Tipo de ficha:** `attr_cstype` (0=PJ, 1=ameaça/NPC, 2=modificadores globais,
   3=domínios). Fase 3 (monstros) usa cstype=1 + campos `attr_menace_*`.

## Cabeçalho
| Nosso campo | Roll20 |
|---|---|
| cabecalho.nome | attr_character_name |
| cabecalho.jogador | attr_playername |
| cabecalho.raca | attr_trace |
| cabecalho.origem | attr_torigin |
| classes[0].nome + nível | attr_tlevel (texto livre) |
| cabecalho.nivel_total | attr_charnivel |
| cabecalho.xp.atual | attr_xp |
| cabecalho.deus | attr_divindade |

## Atributos
| atributos.forca | attr_for |
| atributos.destreza | attr_des |
| atributos.constituicao | attr_con |
| atributos.inteligencia | attr_int |
| atributos.sabedoria | attr_sab |
| atributos.carisma | attr_car |
(❓ validar: input "fake-mod" recebe valor do atributo ou modificador?)

## Status
| status.pv.maximo | attr_vidatotal |
| status.pv.atual | attr_vida |
| status.pm.maximo | attr_manatotal |
| status.pm.atual | attr_mana |
| PV/PM temporários | attr_vidatemp / attr_manatemp |
| status.defesa.total | ⚠️ worker (defesatotal); ajustar via attr_defesaoutros |
| status.deslocamento | attr_deslocamento |
| descricao.tamanho | attr_tamanho (select: 0 Médio, 2 Pequeno, -2 Grande, 5 Minúsculo, -5 Enorme, -10 Colossal) |

## Defesa (partes editáveis)
- attr_modatributodefesa (select: for_mod|des_mod|con_mod|int_mod|sab_mod|car_mod)
- attr_defesaatributo (1=soma DES, 0=não)
- attr_defesaoutros (nossos bônus extras)
- Armadura: attr_armadura1 / attr_armaduradefesa1 / attr_armadurapenalidade1
- Escudo:  attr_armadura2 / attr_armaduradefesa2 / attr_armadurapenalidade2

## Perícias (por perícia <p>)
- Treino: attr_<p>_treinada (checkbox value 1)
- Atributo-chave: attr_<p>atributo2 (select com fórmulas @{for_mod}+@{condicaoperfisico}...)
- Extras: attr_<p>outros (diferença se nosso motor ≠ worker)
- Total: attr_<p>total → NÃO ESCREVER
Nomes: acrobacia, adestramento, atletismo, atuacao, cavalgar, conhecimento, cura,
diplomacia, enganacao, fortitude, furtividade, guerra, iniciativa, intimidacao,
intuicao, investigacao, jogatina, ladinagem, luta, misticismo, nobreza,
oficio (+attr_oficionome), oficio2 (+attr_oficio2nome), percepcao, pilotagem,
pontaria, reflexos, religiao, sobrevivencia, vontade
Perícias extras: repeating_skills → attr_periciaextra / attr_periciaextraoutros /
attr_periciaextratreinada / attr_periciaextraatributo2

## Ataques (repeating_attacks)
attr_nomeataque, attr_bonusataque, attr_danoataque, attr_danoextraataque,
attr_dadoextraataque, attr_margemcriticoataque, attr_multiplicadorcriticoataque,
attr_ataquetipodedano, attr_ataquealcance, attr_ataquedescricao,
attr_ataquepericia (select: @{lutatotal}…|@{pontariatotal}…|@{atuacaototal}…),
attr_modatributodano (select), attr_tipocritico (select)

## Habilidades & Poderes
- repeating_abilities: attr_nameability, attr_skillexecucao, attr_skillpm,
  attr_skillfonte, attr_abilitydescription
- repeating_powers: attr_namepower, attr_skillexecucao, attr_skillpm,
  attr_skillfonte, attr_powerdescription

## Magias (repeating_spells1..5, um grupo por círculo)
attr_namespell, attr_spelltipo (escola), attr_spellexecucao, attr_spellalcance,
attr_spellduracao, attr_spellalvoarea, attr_spellresistencia, attr_spelldescription
CD: attr_cdatributo (select), attr_cdequips, attr_cdpoderes, attr_cdoutros

## Equipamento (repeating_equipment)
attr_equipname, attr_equipquantity, attr_equipslot, attr_eqpdescription
Dinheiro: attr_ts (Tibar), attr_to (T. Ouro)
Carga: attr_carga / attr_limite / attr_maxima → NÃO ESCREVER (readonly)

## Textos
- attr_proficiencias (textarea)
- attr_charnotes (anotações)

## Condições (checkboxes value 1)
attr_abalado, attr_agarrado, attr_alquebrado, attr_apavorado, attr_atordoado,
attr_caido, attr_cego, attr_confuso, attr_debilitado, attr_desprevenido,
attr_doente, attr_emchama, attr_enfeiticado, attr_enjoado, attr_enreado,
attr_envenenado, attr_esmorecido, attr_exausto, attr_fascinado, attr_fatigado,
attr_fraco, attr_frustrado, attr_imovel, attr_inconsciente, attr_indefeso,
attr_lento, attr_ofuscado, attr_paralizado, attr_pasmo, attr_petrificacao,
attr_sangrando, attr_surdo, attr_surpreendido, attr_vulneravel

## Fase 3 — NPCs/Monstros (cstype=1)
attr_menace_name, attr_menace_nd, attr_menace_type_size, attr_menace_hp,
attr_menace_mp, attr_menace_defense, attr_menace_percep, attr_menace_perception,
attr_menace_fortitude, attr_menace_reflex, attr_menace_will,
attr_menace_for/des/con/int/sab/car, attr_menace_desloc,
repeating_menaceabilities (attr_menacenameabilityinput + attr_menaceabilitydescriptioninput),
repeating_menacespells (attr_menacenamespellsinput + attr_menaceaspellsdescriptioninput),
repeating_menacemelee / repeating_menacedistance (ataques ocultos),
attr_menace_treasure, attr_menace_treasures

## ❓ Validar em jogo (quando construir a ponte)
- [ ] attr_for..attr_car: escrever valor do atributo ou modificador?
- [ ] attr_bonus_treino (value 2 no HTML): confirmar regra de treino JdA por nível
- [ ] Criação de linha repeating via setAttrs com ID gerado vs clique no +Add
- [ ] Tempo de recompute dos workers após setAttrs (a ponte precisa aguardar?)
