const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const typingIndicator = document.getElementById('typing-indicator');

// Scroll chat to end
function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Simple Markdown Link Parser
function parseMarkdown(text) {
    // Handle specific bold syntax
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Handle [text](url) links
    text = text.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" class="ticket-link">$1</a>');
    // Handle newlines
    return text.replace(/\n/g, '<br>');
}

// Append message to UI
function appendMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    
    // Parse the text for our custom Markdown features
    const formattedContent = parseMarkdown(text);
    
    messageDiv.innerHTML = `<div class="content">${formattedContent}</div>`;
    
    chatBox.appendChild(messageDiv);
    scrollToBottom();
}

// Handle Quick Action Buttons
function quickAction(text) {
    userInput.value = text;
    sendMessage();
}

// Main Send Function
async function sendMessage() {
    const msg = userInput.value.trim();
    if (!msg) return;

    appendMessage(msg, 'user');
    userInput.value = '';

    typingIndicator.style.display = 'block';
    scrollToBottom();

    try {
        const formData = new FormData();
        formData.append('msg', msg);

        const response = await fetch('/get', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        // Slight delay to feel more natural
        setTimeout(() => {
            typingIndicator.style.display = 'none';
            appendMessage(data.response, 'bot');
        }, 600);
        
    } catch (error) {
        console.error('Error:', error);
        typingIndicator.style.display = 'none';
        appendMessage("Adhii is resting. Please try again in a bit!", 'bot');
    }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
