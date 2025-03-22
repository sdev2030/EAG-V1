chrome.action.onClicked.addListener((tab) => {
    if (!tab.url.includes('chrome://')) {
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            function: () => {
                // Trigger translation when extension icon is clicked
                translateRandomText();
            }
        });
    }
}); 