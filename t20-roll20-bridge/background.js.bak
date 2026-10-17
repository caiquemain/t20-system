console.log('[bridge:bg] service worker v4 (save via modelos Roll20)');

// Função injetada no MAIN world (tem acesso ao window.Campaign da página)
async function fillRoll20ViaModels(ficha) {
  const findCharId = () => {
    const m = location.pathname.match(/\/editor\/character\/[^/]+\/([^/]+)/);
    if (m) return decodeURIComponent(m[1]);
    const iframe = document.querySelector('iframe[name^="iframe_"]');
    if (iframe) return iframe.name.replace('iframe_', '');
    const el = document.querySelector('[data-characterid]');
    if (el) return el.getAttribute('data-characterid');
    return null;
  };
  const charId = findCharId();
  if (!charId) return { ok: false, err: 'characterId não encontrado nesta janela' };

  for (let i = 0; i < 100 && !window.Campaign; i++) await new Promise(r => setTimeout(r, 100));
  if (!window.Campaign) return { ok: false, err: 'window.Campaign indisponível' };
  const character = window.Campaign.characters.get(charId);
  if (!character) return { ok: false, err: 'personagem não está no Campaign desta janela' };

  await new Promise(res => character.attribs.fetch({ success: res, error: res }));
  const byName = {};
  character.attribs.models.forEach(a => { byName[a.get('name')] = a; });

  let n = 0;
  const setAttr = (name, current) => {
    const v = String(current ?? '');
    if (byName[name]) byName[name].save({ current: v });
    else byName[name] = character.attribs.create({ name, current: v });
    n++;
  };

  // UUID no formato Roll20 (copiado do projeto de referência)
  const generateUUID = () => {
    const source = '-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz';
    const getFirstPart = (part, seed) => {
      if (seed === 0) return `-${part}`;
      return getFirstPart(`${source.charAt(seed % 64)}${part}`, Math.floor(seed / 64));
    };
    const getSecondPart = (part, size) => {
      if (part.length === size) return part;
      return getSecondPart(`${part}${source.charAt(Math.floor(64 * Math.random()))}`, size);
    };
    return `${getFirstPart('', new Date().getTime())}${getSecondPart('', 12)}`;
  };

  const rowIdsOf = group => {
    const ids = new Set();
    const re = new RegExp('^' + group + '_([^_]+)_');
    Object.keys(byName).forEach(name => { const m = name.match(re); if (m) ids.add(m[1]); });
    return [...ids];
  };
  const clearGroup = group => {
    rowIdsOf(group).forEach(id => {
      Object.keys(byName).filter(name => name.startsWith(group + '_' + id + '_')).forEach(name => {
        try { byName[name].destroy(); } catch (e) {}
        delete byName[name];
      });
    });
  };
  const addRow = (group, fields) => {
    const id = generateUUID().replace(/_/g, 'Z');
    Object.entries(fields).forEach(([k, v]) => setAttr(`${group}_${id}_${k}`, v));
  };

  // ── Campos simples ──
  const c = ficha.cabecalho || {}, a = ficha.atributos || {}, s = ficha.status || {};
  const TAM = { 'Minúsculo': '5', 'Pequeno': '2', 'Médio': '0', 'Grande': '-2', 'Enorme': '-5', 'Colossal': '-10' };
  setAttr('character_name', c.nome || '');
  setAttr('playername', c.jogador || '');
  setAttr('trace', c.raca || '');
  setAttr('torigin', c.origem || '');
  setAttr('tlevel', `${ficha.classes?.[0]?.nome || ''} ${ficha.classes?.[0]?.nivel || 1}`);
  setAttr('charnivel', ficha.classes?.[0]?.nivel || 1);
  setAttr('xp', c.xp?.atual ?? 0);
  setAttr('divindade', c.deus || '');
  setAttr('for', a.forca ?? 0); setAttr('des', a.destreza ?? 0); setAttr('con', a.constituicao ?? 0);
  setAttr('int', a.inteligencia ?? 0); setAttr('sab', a.sabedoria ?? 0); setAttr('car', a.carisma ?? 0);
  setAttr('vidatotal', s.pv?.maximo ?? 0); setAttr('vida', s.pv?.atual ?? s.pv?.maximo ?? 0);
  setAttr('manatotal', s.pm?.maximo ?? 0); setAttr('mana', s.pm?.atual ?? s.pm?.maximo ?? 0);
  setAttr('deslocamento', `${s.deslocamento ?? 9}m`);
  setAttr('tamanho', TAM[ficha.descricao?.tamanho] ?? '0');
  setAttr('proficiencias', ficha.descricao?.anotacoes || '');
  setAttr('charnotes', ficha.descricao?.historia || '');

  // ── Perícias: treino + atributo-chave + diff em "outros" ──
  const SKILL_MAP = {
    acrobacia: 'Acrobacia', adestramento: 'Adestramento', atletismo: 'Atletismo',
    atuacao: 'Atuação', cavalgar: 'Cavalgar', conhecimento: 'Conhecimento',
    cura: 'Cura', diplomacia: 'Diplomacia', enganacao: 'Enganação',
    fortitude: 'Fortitude', furtividade: 'Furtividade', guerra: 'Guerra',
    iniciativa: 'Iniciativa', intimidacao: 'Intimidação', intuicao: 'Intuição',
    investigacao: 'Investigação', jogatina: 'Jogatina', ladinagem: 'Ladinagem',
    luta: 'Luta', misticismo: 'Misticismo', nobreza: 'Nobreza',
    percepcao: 'Percepção', pilotagem: 'Pilotagem', pontaria: 'Pontaria',
    reflexos: 'Reflexos', religiao: 'Religião', sobrevivencia: 'Sobrevivência',
    vontade: 'Vontade'
  };
  const DEFAULT_ATTR = {
    acrobacia: 'destreza', adestramento: 'carisma', atletismo: 'forca',
    atuacao: 'carisma', cavalgar: 'destreza', conhecimento: 'inteligencia',
    cura: 'sabedoria', diplomacia: 'carisma', enganacao: 'carisma',
    fortitude: 'constituicao', furtividade: 'destreza', guerra: 'inteligencia',
    iniciativa: 'destreza', intimidacao: 'carisma', intuicao: 'sabedoria',
    investigacao: 'inteligencia', jogatina: 'carisma', ladinagem: 'destreza',
    luta: 'forca', misticismo: 'inteligencia', nobreza: 'inteligencia',
    percepcao: 'sabedoria', pilotagem: 'destreza', pontaria: 'destreza',
    reflexos: 'destreza', religiao: 'sabedoria', sobrevivencia: 'sabedoria',
    vontade: 'sabedoria'
  };
  const ATTR_OPT = {
    forca: '@{for_mod} + @{condicaoperfisico} + @{condicaocego}',
    destreza: '@{des_mod} + @{condicaoperfisico} + @{condicaocego}',
    constituicao: '@{con_mod} + @{condicaoperfisico}',
    inteligencia: '@{int_mod} + @{condicaopermental}',
    sabedoria: '@{sab_mod} + @{condicaopermental}',
    carisma: '@{car_mod} + @{condicaopermental}'
  };
  const modsAttr = {
    forca: a.forca ?? 0, destreza: a.destreza ?? 0, constituicao: a.constituicao ?? 0,
    inteligencia: a.inteligencia ?? 0, sabedoria: a.sabedoria ?? 0, carisma: a.carisma ?? 0
  };
  const metadeNivel = Math.floor((ficha.classes?.[0]?.nivel || 1) / 2);
  const periciasNosso = ficha.pericias || {};
  let skillsSync = 0;
  Object.entries(SKILL_MAP).forEach(([slug, nomeNosso]) => {
    const p = periciasNosso[nomeNosso];
    if (!p) return;
    const treino = (p.treino ?? 0) > 0 ? 1 : 0;
    const attrKey = p.atributo || DEFAULT_ATTR[slug];
    setAttr(slug + '_treinada', treino ? '1' : '0');
    setAttr(slug + 'atributo2', ATTR_OPT[attrKey] || ATTR_OPT[DEFAULT_ATTR[slug]]);
    // diff: total da ficha Roll20 = total do nosso motor (regra de ouro)
    const esperadoSheet = metadeNivel + (modsAttr[attrKey] ?? 0) + (treino ? 2 : 0);
    const diff = (p.total ?? 0) - esperadoSheet;
    setAttr(slug + 'outros', diff);
    skillsSync++;
  });
  console.log('[bridge-main] perícias sincronizadas:', skillsSync);

  // ── Ataques (repeating_attacks) ──
  const PERICIA_ATQ = {
    'Luta': '@{lutatotal}+@{condicaomodataquecc}+@{condicaomodataque}',
    'Pontaria': '@{pontariatotal}+@{condicaomodataquedis}+@{condicaomodataque}',
    'Atuação': '@{atuacaototal}+@{condicaomodataquecc}+@{condicaomodataque}'
  };
  clearGroup('repeating_attacks');
  (ficha.combate?.ataques || []).slice(0, 10).forEach(at => {
    const crit = String(at.critico || '');
    let margem = 20, mult = 2;
    if (crit.includes('/')) {
      const [m, x] = crit.split('/');
      if (m && !isNaN(parseInt(m))) margem = parseInt(m);
      if (x) mult = parseInt(x.replace('x', '')) || 2;
    } else if (crit.startsWith('x')) mult = parseInt(crit.replace('x', '')) || 2;
    else if (crit && !isNaN(parseInt(crit))) margem = parseInt(crit);
    addRow('repeating_attacks', {
      nomeataque: at.nome || '', bonusataque: at.bonus_ataque ?? 0, danoataque: at.dano || '',
      margemcriticoataque: margem, multiplicadorcriticoataque: mult,
      ataquetipodedano: at.tipo || '', ataquealcance: at.alcance || '',
      ataquepericia: PERICIA_ATQ[at.teste] || PERICIA_ATQ['Luta']
    });
  });

  // ── Habilidades & Poderes ──
  clearGroup('repeating_abilities');
  clearGroup('repeating_powers');
  (ficha.habilidades || []).forEach(h => {
    const campos = {
      skillexecucao: h.execucao || '', skillpm: h.custo_pm ?? h.pm ?? '',
      skillfonte: h.tipo || ''
    };
    if ((h.tipo || '').includes('Poder')) {
      addRow('repeating_powers', { namepower: h.nome || '', powerdescription: h.descricao || '', ...campos });
    } else {
      addRow('repeating_abilities', { nameability: h.nome || '', abilitydescription: h.descricao || '', ...campos });
    }
  });

  // ── Magias por círculo (repeating_spells1..5) ──
  for (let circ = 1; circ <= 5; circ++) clearGroup('repeating_spells' + circ);
  (ficha.combate?.magias || []).forEach(mg => {
    const circ = Math.min(Math.max(parseInt(mg.circulo) || 1, 1), 5);
    addRow('repeating_spells' + circ, {
      namespell: mg.nome || '', spelltipo: mg.escola || mg.tipo || '',
      spellexecucao: mg.execucao || '', spellalcance: mg.alcance || '',
      spellduracao: mg.duracao || '', spellalvoarea: mg.alvo_area || mg.alvo || '',
      spellresistencia: mg.resistencia || '', spelldescription: mg.descricao || ''
    });
  });

  // ── Equipamentos ──
  clearGroup('repeating_equipment');
  (ficha.inventario?.equipamentos || []).slice(0, 40).forEach(eq => {
    addRow('repeating_equipment', {
      equipname: eq.nome || '', equipquantity: eq.qtd ?? 1,
      equipslot: eq.espaco ?? 0, eqpdescription: ''
    });
  });

  // ── Nome do personagem: caminho especial ──
  // @{character_name} é referência reservada do Roll20: a view da ficha
  // sincroniza o input com o MODELO do character, não com o atributo.
  try {
    const nomeNosso = (ficha.cabecalho || {}).nome || '';
    if (nomeNosso) character.save({ name: nomeNosso });
    setAttr('charname', nomeNosso);
  } catch (e) {}
  // Fallback DOM: reproduz o caminho de edição manual via jQuery da página
  try {
    const $ = window.jQuery || window.$;
    const domSet = (sel, v) => {
      const el = document.querySelector(sel);
      if (el && $) { el.value = String(v ?? ''); $(el).trigger('change'); }
    };
    domSet('form.sheetform [name="attr_character_name"]', (ficha.cabecalho || {}).nome || '');
    domSet('form.sheetform [name="attr_playername"]', (ficha.cabecalho || {}).jogador || '');
  } catch (e) {}

  // ── Nome do personagem: caminho especial ──
  // @{character_name} é referência reservada do Roll20: a view da ficha
  // sincroniza o input com o MODELO do character, não com o atributo.
  try {
    const nomeNosso = (ficha.cabecalho || {}).nome || '';
    if (nomeNosso) character.save({ name: nomeNosso });
    setAttr('charname', nomeNosso);
  } catch (e) {}
  // Fallback DOM: reproduz o caminho de edição manual via jQuery da página
  try {
    const $ = window.jQuery || window.$;
    const domSet = (sel, v) => {
      const el = document.querySelector(sel);
      if (el && $) { el.value = String(v ?? ''); $(el).trigger('change'); }
    };
    domSet('form.sheetform [name="attr_character_name"]', (ficha.cabecalho || {}).nome || '');
    domSet('form.sheetform [name="attr_playername"]', (ficha.cabecalho || {}).jogador || '');
  } catch (e) {}

  // ── Dinheiro (Tibar): a ficha principal TEM campo, então sincroniza ──
  const din = ficha.inventario?.dinheiro || {};
  setAttr('ts', din.tl ?? 0); // T$ prata (Tibar padrão da ficha JdA)
  setAttr('to', din.to ?? 0); // T. Ouro
  // cobre (tp) não tem campo na ficha JdA oficial — ignorado de propósito

  return { ok: true, charId, attrs: n };
}

async function runFillInTab(tabId, ficha) {
  try {
    const res = await chrome.scripting.executeScript({
      target: { tabId }, world: 'MAIN', func: fillRoll20ViaModels, args: [ficha]
    });
    return (res && res[0] && res[0].result) || { ok: false, err: 'sem resultado' };
  } catch (e) {
    return { ok: false, err: String(e) };
  }
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === 'FICHA_PARA_ROLL20') {
    chrome.storage.local.set({ pontePendente: msg.ficha, ponteTs: Date.now() }, async () => {
      const tabs = await chrome.tabs.query({ url: 'https://app.roll20.net/*' });
      console.log('[bridge:bg] abas roll20:', tabs.length);
      const results = [];
      for (const t of tabs) results.push({ tab: t.id, url: t.url, r: await runFillInTab(t.id, msg.ficha) });
      console.log('[bridge:bg] resultados:', results);
      const ok = results.find(x => x.r && x.r.ok);
      if (ok) chrome.storage.local.remove('pontePendente');
      sendResponse({ ok: !!ok, results });
    });
    return true;
  }
  if (msg.type === 'EXEC_MAIN' && sender.tab && sender.tab.id != null) {
    runFillInTab(sender.tab.id, msg.ficha).then(r => {
      if (r && r.ok) chrome.storage.local.remove('pontePendente');
      sendResponse(r);
    });
    return true;
  }
});
