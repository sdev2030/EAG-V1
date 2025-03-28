// Replace with your actual Gemini API key
const GEMINI_API_KEY = 'Your API key';

async function generateFibonacci(n) {
    const prompt = `Generate the first ${n} Fibonacci numbers as a comma-separated list.`;

    try {
        const response = await fetch(`https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key=${GEMINI_API_KEY}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: prompt
                    }]
                }]
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('API Response:', data); // For debugging

        // Check if we have a valid response
        if (!data || !data.candidates || !data.candidates[0] || !data.candidates[0].content) {
            throw new Error('Invalid response from Gemini API');
        }

        // Extract the text from the response
        const responseText = data.candidates[0].content.parts[0].text;

        // Parse the numbers from the response
        const fibonacciNumbers = responseText
            .split(',')
            .map(num => parseInt(num.trim()))
            .filter(num => !isNaN(num)); // Filter out any invalid numbers

        if (fibonacciNumbers.length === 0) {
            throw new Error('No valid Fibonacci numbers found in response');
        }

        return fibonacciNumbers;
    } catch (error) {
        console.error('Error generating Fibonacci numbers:', error);
        throw error;
    }
}

function calculateExponentialSum(numbers) {
    return numbers.reduce((sum, num) => sum + Math.exp(num), 0);
}

document.getElementById('calculate').addEventListener('click', async () => {
    const fibCount = parseInt(document.getElementById('fibCount').value);
    const resultDiv = document.getElementById('result');

    if (fibCount < 1 || fibCount > 20) {
        resultDiv.textContent = 'Please enter a number between 1 and 20';
        return;
    }

    try {
        resultDiv.textContent = 'Calculating...';
        const fibonacciNumbers = await generateFibonacci(fibCount);
        const sum = calculateExponentialSum(fibonacciNumbers);

        resultDiv.innerHTML = `
      <strong>Fibonacci Numbers:</strong> ${fibonacciNumbers.join(', ')}<br>
      <strong>Sum of Exponentials:</strong> ${sum.toFixed(2)}
    `;
    } catch (error) {
        resultDiv.textContent = 'Error calculating result. Please try again.';
    }
}); 