(function () {
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
    if (!id) return alert('ID da ficha não encontrado na URL.');
    btn.textContent = '⏳ Buscando ficha...';
    try {
      const resp = await fetch(`http://localhost:8000/personagens/${id}`);
      if (!resp.ok) throw new Error('API respondeu ' + resp.status);
      const ficha = await resp.json();
      chrome.runtime.sendMessage({ type: 'FICHA_PARA_ROLL20', ficha }, () => {
        reset('✅ Enviada! Abra a ficha no Roll20', 4000);
      });
    } catch (e) {
      reset('❌ Erro ao buscar', 3000);
      alert('Erro ao buscar ficha: ' + e.message);
    }
  };
})();
