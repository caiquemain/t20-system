(function () {
  const MAPA_TAMANHO = { 'Minúsculo': '5', 'Pequeno': '2', 'Médio': '0', 'Grande': '-2', 'Enorme': '-5', 'Colossal': '-10' };
  let avisou = false; // warn 1x por janela (sem spam)

  // setAttr em TODOS os elementos com o name (corrige campos duplicados: charnivel x2)
  function setAttr(nome, valor) {
    const els = document.querySelectorAll(`[name="attr_${nome}"]`);
    if (!els.length) return false;
    els.forEach(el => {
      if (el.tagName === 'SELECT') el.value = String(valor);
      else if (el.type === 'checkbox') el.checked = Boolean(valor);
      else el.value = String(valor);
      el.dispatchEvent(new Event('change', { bubbles: true }));
    });
    return true;
  }

  function preencher(ficha) {
    if (!document.querySelector('form.sheetform')) {
      if (!avisou) {
        console.warn('[bridge] ficha JdA não está aberta NESTA janela — ignorando silenciosamente.');
        avisou = true;
      }
      return false;
    }
    const ok = [], falhas = [];
    const set = (nome, valor) => (setAttr(nome, valor) ? ok : falhas).push(nome);

    const c = ficha.cabecalho || {};
    const a = ficha.atributos || {};
    const s = ficha.status || {};

    // Cabeçalho
    set('character_name', c.nome || '');
    set('playername', c.jogador || '');
    set('trace', c.raca || '');
    set('torigin', c.origem || '');
    set('tlevel', `${ficha.classes?.[0]?.nome || ''} ${ficha.classes?.[0]?.nivel || 1}`);
    set('charnivel', ficha.classes?.[0]?.nivel || 1);   // agora pega os 2 inputs
    set('xp', c.xp?.atual ?? 0);
    set('divindade', c.deus || '');

    // Atributos (T20 JdA: valor = modificador)
    set('for', a.forca ?? 0);
    set('des', a.destreza ?? 0);
    set('con', a.constituicao ?? 0);
    set('int', a.inteligencia ?? 0);
    set('sab', a.sabedoria ?? 0);
    set('car', a.carisma ?? 0);

    // Status
    set('vidatotal', s.pv?.maximo ?? 0);
    set('vida', s.pv?.atual ?? s.pv?.maximo ?? 0);
    set('manatotal', s.pm?.maximo ?? 0);
    set('mana', s.pm?.atual ?? s.pm?.maximo ?? 0);
    set('deslocamento', `${s.deslocamento ?? 9}m`);
    set('tamanho', MAPA_TAMANHO[ficha.descricao?.tamanho] ?? '0');

    // Textos
    set('proficiencias', ficha.descricao?.anotacoes || '');
    set('charnotes', ficha.descricao?.historia || '');

    console.log(`[bridge] ✅ preenchidos: ${ok.length} | ❌ não encontrados: ${falhas.length}`, falhas);
    return true;
  }

  // Via mensagem do background (aba/popup já com ficha aberta)
  chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.type !== 'PREENCHER') return;
    const feito = preencher(msg.ficha);
    if (feito) chrome.storage.local.remove('pontePendente');
    sendResponse({ ok: feito });
  });

  // Via storage: observer SÓ age quando o form existir, e desliga após sucesso/limite
  chrome.storage.local.get('pontePendente', (r) => {
    if (!r.pontePendente) return;
    let tentativas = 0;
    const obs = new MutationObserver(() => {
      if (!document.querySelector('form.sheetform')) return; // não loga spam
      if (++tentativas > 50) { obs.disconnect(); return; }
      if (preencher(r.pontePendente)) {
        chrome.storage.local.remove('pontePendente');
        obs.disconnect();
      }
    });
    obs.observe(document.body, { childList: true, subtree: true });
    setTimeout(() => obs.disconnect(), 60000);
    // tentativa imediata (caso a ficha já esteja aberta)
    if (preencher(r.pontePendente)) chrome.storage.local.remove('pontePendente');
  });
})();
