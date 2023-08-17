const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const chatBotSelector = document.getElementById('chat-bot-selector');

function displayUserMessage(message) {
    const userMessage = document.createElement('div');
    userMessage.classList.add('chat-message');
    userMessage.textContent = message;
    chatBox.appendChild(userMessage);
}

function displayBotMessage(message) {
    const botMessage = document.createElement('div');
    botMessage.classList.add('chat-message', 'bot-message');
    botMessage.textContent = message;
    chatBox.appendChild(botMessage);

    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;
}

userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent the default behavior (e.g., line break)
        sendMessage(); // Call the function to send the message
    }
});

sendButton.addEventListener('click', () => {
    sendMessage(); // Call the function to send the message
});

chatBotSelector.addEventListener('change', () => {
    // Change the URL based on the selected chat bot
    const selectedChatBot = chatBotSelector.value;
    const url = `http://localhost:${selectedChatBot === 'chatbot1' ? 8000 : 8001}`;

    sendButton.setAttribute('data-url', url);
});

async function sendMessage() {
    const message = userInput.value;
    if (message.trim() === '') return;

    displayUserMessage(message);
    userInput.value = '';

    try {
        const url = sendButton.getAttribute('data-url'); // Get the URL from the button attribute

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        const responseData = await response.json();
        const botResponse = responseData.bot_response;

        displayBotMessage(botResponse);
    } catch (error) {
        console.error('Error:', error);
    }

    // Scroll to the bottom of the chat box after sending the message
    chatBox.scrollTop = chatBox.scrollHeight;
}
