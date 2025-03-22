async function translateText(text) {
    try {
        const API_KEY = 'Your API Key';
        const geminiResponse = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${API_KEY}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `You are a direct translator. Translate to French without any additional text or explanation: ${text}`
                    }]
                }],
                generationConfig: {
                    temperature: 0.1,
                    topK: 1,
                    topP: 1
                }
            })
        });

        if (!geminiResponse.ok) {
            throw new Error(`Gemini API error: ${geminiResponse.status}`);
        }

        const geminiData = await geminiResponse.json();
        // Extract just the translated text, removing any extra formatting or explanation
        let translatedText = geminiData.candidates[0].content.parts[0].text;
        // Clean up the response to get only the translated text
        translatedText = translatedText
            .replace(/^['"`]|['"`]$/g, '') // Remove quotes
            .replace(/^Translation:?\s*/i, '') // Remove "Translation:" prefix
            .replace(/^En français:?\s*/i, '') // Remove "En français:" prefix
            .trim();

        return translatedText;
    } catch (error) {
        console.error('Translation error:', error);
        throw error;
    }
}

// Update CSS styles
const style = document.createElement('style');
style.textContent = `
  @keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0.7; }
    100% { opacity: 1; }
  }
  .translated-text {
    color: red;
    animation: blink 2s ease-in-out infinite;
  }
  .translated-text:hover {
    content: attr(data-original);
  }
`;
document.head.appendChild(style);

function getRandomTextNodes() {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    const textNodes = [];
    let node;
    while (node = walker.nextNode()) {
        // Only get text nodes that have actual content and aren't already translated
        const parentElement = node.parentElement;
        if (node.nodeValue.trim().length > 0 &&
            !parentElement.classList.contains('translated-text') &&
            !['SCRIPT', 'STYLE', 'TEXTAREA'].includes(parentElement.tagName)) {
            textNodes.push(node);
        }
    }
    return textNodes;
}

async function translateRandomText() {
    const textNodes = getRandomTextNodes();
    if (textNodes.length === 0) return;

    const randomIndex = Math.floor(Math.random() * textNodes.length);
    const randomNode = textNodes[randomIndex];
    const originalText = randomNode.nodeValue.trim();

    try {
        const translatedText = await translateText(originalText);

        const span = document.createElement('span');
        span.className = 'translated-text';
        span.textContent = translatedText;
        span.setAttribute('data-original', originalText);
        span.addEventListener('mouseover', (e) => {
            e.target.textContent = originalText;
        });
        span.addEventListener('mouseout', (e) => {
            e.target.textContent = translatedText;
        });

        randomNode.parentNode.replaceChild(span, randomNode);
    } catch (error) {
        console.error('Translation error:', error);
    }
}

// Start translation
translateRandomText(); 