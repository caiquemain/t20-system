(function () {
  console.log('[bridge:roll20] content script (isolated) v4 em', location.href);

  const charIdVisivel = (() => {
    const m = location.pathname.match(/\/editor\/character\/[^/]+\/([^/]+)/);
    if (m) return m[1];
    const iframe = document.querySelector('iframe[name^="iframe_"]');
    if (iframe) return iframe.name.replace('iframe_', '');
    return null;
  })();

  const pedirExec = ficha => chrome.runtime.sendMessage({ type: 'EXEC_MAIN', ficha },
    r => console.log('[bridge:roll20] resultado MAIN world:', r));

  chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.type === 'PREENCHER') { pedirExec(msg.ficha); sendResponse({ ok: true, delegated: 'MAIN world' }); }
  });

  // Aba aberta depois do envio: pega payload pendente e executa
  chrome.storage.local.get('pontePendente', r => {
    if (r.pontePendente && charIdVisivel) {
      console.log('[bridge:roll20] payload pendente + ficha detectada → executando');
      pedirExec(r.pontePendente);
    }
  });
})();
