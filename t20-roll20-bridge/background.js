console.log('[bridge:bg] service worker v4 (PJ + Ameaças)');

// =====================================================================
// FUNÇÃO DE PREENCHIMENTO (PJ e AMEAÇA)
// =====================================================================
async function fillRoll20(ficha, isMenace = false) {
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

  const generateUUID = () => {
    const source = '-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz';
    const getFirstPart = (part, seed) => seed === 0 ? `-${part}` : getFirstPart(`${source.charAt(seed % 64)}${part}`, Math.floor(seed / 64));
    const getSecondPart = (part, size) => part.length === size ? part : getSecondPart(`${part}${source.charAt(Math.floor(64 * Math.random()))}`, size);
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

  if (isMenace) {
    // ── Lógica para AMEAÇA (Mapeada para Ficha de Jogador) ──
    setAttr('cstype', 0); // Força aba PJ
    setAttr('character_name', ficha.nome || '');
    setAttr('trace', `${ficha.tipo}${ficha.subtipo ? ' ('+ficha.subtipo+')' : ''}`);
    setAttr('tlevel', `ND ${ficha.nd}`);
    setAttr('charnivel', parseInt(ficha.nd) || 1);
    setAttr('xp', 0);

    const at = ficha.atributos || {};
    const aFor = at.forca ?? 0, aDes = at.destreza ?? 0, aCon = at.constituicao ?? 0;
    const aInt = at.inteligencia ?? 0, aSab = at.sabedoria ?? 0, aCar = at.carisma ?? 0;
    setAttr('for', aFor); setAttr('des', aDes); setAttr('con', aCon);
    setAttr('int', aInt); setAttr('sab', aSab); setAttr('car', aCar);

    setAttr('vidatotal', ficha.pontos_de_vida ?? 0);
    setAttr('vida', ficha.pontos_de_vida ?? 0);
    setAttr('vidatemp', 0);
    setAttr('manatotal', ficha.pontos_de_mana ?? 0);
    setAttr('mana', ficha.pontos_de_mana ?? 0);
    setAttr('manatemp', 0);
    
    const defesaOutros = (ficha.defesa ?? 10) - 10 - aDes;
    setAttr('defesaoutros', defesaOutros);
    setAttr('modatributodefesa', 'des_mod');
    setAttr('defesaatributo', 1);

    setAttr('deslocamento', ficha.deslocamento || '9m');
    const TAM = { 'Minúsculo': '5', 'Pequeno': '2', 'Médio': '0', 'Grande': '-2', 'Enorme': '-5', 'Colossal': '-10' };
    setAttr('tamanho', TAM[ficha.tamanho] ?? '0');

    const SKILL_SLUG = {
      'Acrobacia': 'acrobacia', 'Adestramento': 'adestramento', 'Atletismo': 'atletismo',
      'Atuação': 'atuacao', 'Cavalgar': 'cavalgar', 'Conhecimento': 'conhecimento',
      'Cura': 'cura', 'Diplomacia': 'diplomacia', 'Enganação': 'enganacao',
      'Fortitude': 'fortitude', 'Furtividade': 'furtividade', 'Guerra': 'guerra',
      'Iniciativa': 'iniciativa', 'Intimidação': 'intimidacao', 'Intuição': 'intuicao',
      'Investigação': 'investigacao', 'Jogatina': 'jogatina', 'Ladinagem': 'ladinagem',
      'Luta': 'luta', 'Misticismo': 'misticismo', 'Nobreza': 'nobreza',
      'Percepção': 'percepcao', 'Pilotagem': 'pilotagem', 'Pontaria': 'pontaria',
      'Reflexos': 'reflexos', 'Religião': 'religiao', 'Sobrevivência': 'sobrevivencia',
      'Vontade': 'vontade'
    };
    const DEFAULT_ATTR = {
      acrobacia: 'destreza', adestramento: 'carisma', atletismo: 'forca', atuacao: 'carisma', cavalgar: 'destreza',
      conhecimento: 'inteligencia', cura: 'sabedoria', diplomacia: 'carisma', enganacao: 'carisma', fortitude: 'constituicao',
      furtividade: 'destreza', guerra: 'inteligencia', iniciativa: 'destreza', intimidacao: 'carisma', intuicao: 'sabedoria',
      investigacao: 'inteligencia', jogatina: 'carisma', ladinagem: 'destreza', luta: 'forca', misticismo: 'inteligencia',
      nobreza: 'inteligencia', percepcao: 'sabedoria', pilotagem: 'destreza', pontaria: 'destreza', reflexos: 'destreza',
      religiao: 'sabedoria', sobrevivencia: 'sabedoria', vontade: 'sabedoria'
    };
    const modsAttr = { forca: aFor, destreza: aDes, constituicao: aCon, inteligencia: aInt, sabedoria: aSab, carisma: aCar };
    const metadeNivel = Math.floor((parseInt(ficha.nd) || 1) / 2);
    
    (ficha.pericias || []).forEach(p => {
      const slug = SKILL_SLUG[p.nome];
      if (!slug) return;
      const attrKey = DEFAULT_ATTR[slug] || 'destreza';
      setAttr(`${slug}_treinada`, 1);
      const esperado = metadeNivel + (modsAttr[attrKey] ?? 0) + 2;
      setAttr(`${slug}_outros`, (p.bonus ?? 0) - esperado);
    });

    const PERICIA_ATQ = {
      'Luta': '@{lutatotal}+@{condicaomodataquecc}+@{condicaomodataque}',
      'Pontaria': '@{pontariatotal}+@{condicaomodataquedis}+@{condicaomodataque}',
      'Atuação': '@{atuacaototal}+@{condicaomodataquecc}+@{condicaomodataque}'
    };
    
    clearGroup('repeating_attacks');
    (ficha.ataques || []).forEach(a => {
      addRow('repeating_attacks', {
        nomeataque: a.nome || '',
        bonusataque: a.bonus_ataque ?? 0,
        danoataque: a.dano || '',
        margemcriticoataque: a.margem_critico ?? 20,
        multiplicadorcriticoataque: a.multiplicador_critico ?? 2,
        ataquetipodedano: a.tipo_dano || '',
        ataquealcance: a.alcance || '',
        ataquepericia: PERICIA_ATQ[a.pericia] || PERICIA_ATQ['Luta'],
        ataquedescricao: a.descricao ? a.descricao.replace(/(\d+d\d+(?:\s*[+-]\s*\d+)?)/gi, '[[$1]]') : ''
      });
    });

    clearGroup('repeating_abilities');
    clearGroup('repeating_powers');
    (ficha.habilidades || []).forEach(h => {
      const rollsTxt = (h.rolls && h.rolls.length) ? '\n\n' + h.rolls.map(r => `[[${r}]]`).join(' ') : '';
      const desc = (h.descricao || '') + rollsTxt;
      addRow('repeating_abilities', {
        nameability: h.nome || '',
        abilitydescription: desc,
        skillexecucao: h.tipo_acao || '',
        skillpm: h.custo_pm ?? '',
        skillfonte: 'Ameaça'
      });
    });

    for (let c = 1; c <= 5; c++) clearGroup('repeating_spells' + c);
    (ficha.magias || []).forEach(mg => {
      const circ = Math.min(Math.max(parseInt(mg.circulo) || 1, 1), 5);
      addRow('repeating_spells' + circ, {
        namespell: mg.nome || '',
        spelltipo: mg.escola || mg.tipo || '',
        spellexecucao: mg.execucao || '',
        spellalcance: mg.alcance || '',
        spellduracao: mg.duracao || '',
        spellalvoarea: mg.alvo || '',
        spellresistencia: mg.resistencia || '',
        spelldescription: mg.descricao || ''
      });
    });

    try { if (ficha.nome) character.save({ name: ficha.nome }); } catch (e) {}
    
  } else {
    // ── Lógica Original para PERSONAGEM (Mantida intacta) ──
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
    const modsAttr = { forca: a.forca ?? 0, destreza: a.destreza ?? 0, constituicao: a.constituicao ?? 0, inteligencia: a.inteligencia ?? 0, sabedoria: a.sabedoria ?? 0, carisma: a.carisma ?? 0 };
    const metadeNivel = Math.floor((ficha.classes?.[0]?.nivel || 1) / 2);
    const periciasNosso = ficha.pericias || {};
    
    Object.entries(SKILL_MAP).forEach(([slug, nomeNosso]) => {
      const p = periciasNosso[nomeNosso];
      if (!p) return;
      const treino = (p.treino ?? 0) > 0 ? 1 : 0;
      const attrKey = p.atributo || DEFAULT_ATTR[slug];
      setAttr(slug + '_treinada', treino ? '1' : '0');
      setAttr(slug + 'atributo2', ATTR_OPT[attrKey] || ATTR_OPT[DEFAULT_ATTR[slug]]);
      const esperadoSheet = metadeNivel + (modsAttr[attrKey] ?? 0) + (treino ? 2 : 0);
      const diff = (p.total ?? 0) - esperadoSheet;
      setAttr(slug + 'outros', diff);
    });

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

    clearGroup('repeating_equipment');
    (ficha.inventario?.equipamentos || []).slice(0, 40).forEach(eq => {
      addRow('repeating_equipment', {
        equipname: eq.nome || '', equipquantity: eq.qtd ?? 1,
        equipslot: eq.espaco ?? 0, eqpdescription: ''
      });
    });

    try {
      const nomeNosso = (ficha.cabecalho || {}).nome || '';
      if (nomeNosso) character.save({ name: nomeNosso });
      setAttr('charname', nomeNosso);
    } catch (e) {}
    
    const din = ficha.inventario?.dinheiro || {};
    setAttr('ts', din.tl ?? 0);
    setAttr('to', din.to ?? 0);
  }

  return { ok: true, charId, attrs: n };
}

// =====================================================================
// INJEÇÃO E MENSAGERIA
// =====================================================================
async function runFillInTab(tabId, payload, isMenace = false) {
  try {
    const res = await chrome.scripting.executeScript({
      target: { tabId }, world: 'MAIN', func: fillRoll20, args: [payload, isMenace]
    });
    return (res && res[0] && res[0].result) || { ok: false, err: 'sem resultado' };
  } catch (e) {
    return { ok: false, err: String(e) };
  }
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === 'FICHA_PARA_ROLL20') {
    chrome.storage.local.set({ pontePendente: msg.ficha, ponteTs: Date.now(), ponteTipo: 'pj' }, async () => {
      const tabs = await chrome.tabs.query({ url: 'https://app.roll20.net/*' });
      const results = [];
      for (const t of tabs) results.push({ tab: t.id, r: await runFillInTab(t.id, msg.ficha, false) });
      const ok = results.find(x => x.r && x.r.ok);
      if (ok) chrome.storage.local.remove(['pontePendente', 'ponteTipo']);
      sendResponse({ ok: !!ok, results });
    });
    return true;
  }

  if (msg.type === 'AMEACA_PARA_ROLL20') {
    chrome.storage.local.set({ pontePendente: msg.ameaca, ponteTs: Date.now(), ponteTipo: 'ameaca' }, async () => {
      const tabs = await chrome.tabs.query({ url: 'https://app.roll20.net/*' });
      const results = [];
      for (const t of tabs) results.push({ tab: t.id, r: await runFillInTab(t.id, msg.ameaca, true) });
      const ok = results.find(x => x.r && x.r.ok);
      if (ok) chrome.storage.local.remove(['pontePendente', 'ponteTipo']);
      sendResponse({ ok: !!ok, results });
    });
    return true;
  }

  if (msg.type === 'EXEC_MAIN' && sender.tab && sender.tab.id != null) {
    runFillInTab(sender.tab.id, msg.ficha, false).then(r => {
      if (r && r.ok) chrome.storage.local.remove(['pontePendente', 'ponteTipo']);
      sendResponse(r);
    });
    return true;
  }

  if (msg.type === 'EXEC_MAIN_AMEACA' && sender.tab && sender.tab.id != null) {
    runFillInTab(sender.tab.id, msg.ameaca, true).then(r => {
      if (r && r.ok) chrome.storage.local.remove(['pontePendente', 'ponteTipo']);
      sendResponse(r);
    });
    return true;
  }
});
