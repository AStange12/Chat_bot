const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

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


sendButton.addEventListener('click', async () => {
    const message = userInput.value;
    if (message.trim() === '') return;

    displayUserMessage(message);
    userInput.value = '';

    try {
        const response = await fetch('http://localhost:8000', {
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
});
