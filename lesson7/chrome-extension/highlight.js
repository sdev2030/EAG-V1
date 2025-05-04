function highlightText(query) {
    if (!query) return;
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    const ranges = [];
    while (walker.nextNode()) {
      const node = walker.currentNode;
      let idx = node.nodeValue.toLowerCase().indexOf(query.toLowerCase());
      while (idx !== -1) {
        const range = document.createRange();
        range.setStart(node, idx);
        range.setEnd(node, idx + query.length);
        ranges.push(range);
        idx = node.nodeValue.toLowerCase().indexOf(query.toLowerCase(), idx + query.length);
      }
    }
    ranges.reverse().forEach(range => {
      const mark = document.createElement('mark');
      mark.style.background = 'yellow';
      range.surroundContents(mark);
    });
  }
  
  // Listen for messages from the extension
  chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    console.log('Received message in highlight.js:', msg);
    if (msg.action === 'highlight' && msg.query) {
      highlightText(msg.query);
    }
  });