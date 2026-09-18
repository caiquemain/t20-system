chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type !== 'FICHA_PARA_ROLL20') return;

  chrome.storage.local.set({ pontePendente: msg.ficha, ponteTs: Date.now() }, async () => {
    const tabs = await chrome.tabs.query({ url: 'https://app.roll20.net/*' });
    if (tabs.length > 0) {
      await chrome.tabs.update(tabs[0].id, { active: true });
      try {
        chrome.tabs.sendMessage(tabs[0].id, { type: 'PREENCHER', ficha: msg.ficha });
        sendResponse({ ok: true, destino: 'aba existente do Roll20' });
      } catch (e) {
        sendResponse({ ok: true, destino: 'aba existe mas a ficha ainda não carregou — preenchimento automático ao abrir' });
      }
    } else {
      chrome.tabs.create({ url: 'https://app.roll20.net/' });
      sendResponse({ ok: true, destino: 'nova aba — abra a ficha do personagem lá que o preenchimento é automático' });
    }
  });
  return true; // resposta assíncrona
});
