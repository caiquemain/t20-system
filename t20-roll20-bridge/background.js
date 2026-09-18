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
