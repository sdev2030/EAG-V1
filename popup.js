document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('toggleTheme').addEventListener('click', async () => {
        try {
            // Get the active tab
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

            if (!tab) {
                console.error('No active tab found');
                return;
            }

            // Check if the URL is a chrome:// URL
            if (tab.url.startsWith('chrome://')) {
                document.getElementById('toggleTheme').textContent = 'Cannot modify Chrome pages';
                document.getElementById('toggleTheme').disabled = true;
                setTimeout(() => {
                    document.getElementById('toggleTheme').textContent = 'Toggle Dark Mode';
                    document.getElementById('toggleTheme').disabled = false;
                }, 2000);
                return;
            }

            // Execute the script in the active tab
            await chrome.scripting.executeScript({
                target: { tabId: tab.id },
                func: toggleDarkMode
            });
        } catch (error) {
            console.error('Error:', error);
        }
    });
});

function toggleDarkMode() {
    document.body.style.backgroundColor =
        document.body.style.backgroundColor === 'black' ? 'white' : 'black';
    document.body.style.color =
        document.body.style.color === 'white' ? 'black' : 'white';
} 