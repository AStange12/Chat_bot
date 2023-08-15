const http = require('http');
const { spawn } = require('child_process');

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
}

sendButton.addEventListener('click', () => {
    const message = userInput.value;
    if (message.trim() === '') return;

    displayUserMessage(message);
    userInput.value = '';

    // Run the Python script using Node.js child_process
    const pythonProcess = spawn('python', ['chat_bot_1.py', message]);

    pythonProcess.stdout.on('data', (data) => {
        const botResponse = data.toString().trim();
        displayBotMessage(botResponse);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python Error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python process exited with code ${code}`);
    });
});
