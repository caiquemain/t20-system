(function () {
  console.log('[bridge:t20] content script carregado em', location.href);
  if (document.getElementById('t20-bridge-btn')) return;

  const btn = document.createElement('button');
  btn.id = 't20-bridge-btn';
  btn.textContent = '📤 Enviar pro Roll20';
  btn.style.cssText = 'position:fixed;bottom:20px;right:20px;z-index:99999;padding:12px 18px;' +
    'background:#9c27b0;color:#fff;border:none;border-radius:8px;font-weight:bold;cursor:pointer;' +
    'box-shadow:0 4px 12px rgba(0,0,0,.4);font-size:14px;';
  document.body.appendChild(btn);

  const reset = (txt, ms) => { btn.textContent = txt; setTimeout(() => (btn.textContent = '📤 Enviar pro Roll20'), ms); };

  btn.onclick = async () => {
    const id = location.pathname.split('/').filter(Boolean).pop();
    console.log('[bridge:t20] botão clicado, id =', id);
    if (!id) return alert('ID da ficha não encontrado na URL.');
    btn.textContent = '⏳ Buscando ficha...';
    try {
      const resp = await fetch(`http://localhost:8000/personagens/${id}`);
      if (!resp.ok) throw new Error('API respondeu ' + resp.status);
      const ficha = await resp.json();
      console.log('[bridge:t20] ficha obtida:', ficha.cabecalho?.nome, '| nv', ficha.classes?.[0]?.nivel);
      chrome.runtime.sendMessage({ type: 'FICHA_PARA_ROLL20', ficha }, (r) => {
        if (chrome.runtime.lastError) {
          console.error('[bridge:t20] erro sendMessage:', chrome.runtime.lastError.message);
          return reset('❌ Extensão sem conexão', 4000);
        }
        console.log('[bridge:t20] resposta do background:', r);
        if (r && r.ok === false) { alert('Bridge: ' + r.erro); return reset('❌ ' + r.erro, 5000); }
        reset('✅ Enviada! Veja a aba do Roll20', 4000);
      });
    } catch (e) {
      console.error('[bridge:t20] erro fetch:', e);
      reset('❌ Erro ao buscar', 3000);
    }
  };
})();
