window.addEventListener('DOMContentLoaded', () => {
  // Query the active tab in the current window
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    if (tabs && tabs[0] && tabs[0].url) {
      document.getElementById('url').value = tabs[0].url;
    }
  });
});

document.getElementById('search').addEventListener('click', async () => {
  const query = document.getElementById('query').value;
  console.log("Query string is ", query)
  const resultDiv = document.getElementById('result');
  resultDiv.textContent = 'Searching...';

  try {
    const response = await fetch('http://localhost:5000/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });
    const data = await response.json();
    console.log("response received is", data);
    if (data.url) {
      resultDiv.innerHTML = `<a href="${data.url}" target="_blank">${data.url}</a>`;

      chrome.tabs.create({ url: data.url }, (tab) => {
        chrome.tabs.onUpdated.addListener(function listener(tabId, info) {
          if (tabId === tab.id && info.status === 'complete') {
            chrome.tabs.onUpdated.removeListener(listener);
            chrome.scripting.executeScript({
              target: { tabId: tab.id },
              files: ['highlight.js']
            }, () => {
              chrome.tabs.sendMessage(tab.id, { action: 'highlight', query });
            });
          }
        });
      });
    } else {
      resultDiv.textContent = 'No result found.';
    }
  } catch (err) {
    resultDiv.textContent = 'Error connecting to backend.';
  }
});

document.getElementById('index').addEventListener('click', async () => {
  const url = document.getElementById('url').value;
  const resultDiv = document.getElementById('result');
  resultDiv.textContent = 'Indexing...';

  try {
    const response = await fetch('http://localhost:5000/index', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    const data = await response.json();
    if (data.result) {
      resultDiv.textContent = data.result;
    } else {
      resultDiv.textContent = data.error || 'Indexing failed.';
    }
  } catch (err) {
    resultDiv.textContent = 'Error connecting to backend.';
  }
}); 