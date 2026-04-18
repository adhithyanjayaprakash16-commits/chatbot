document.addEventListener('DOMContentLoaded', () => {
    const chatArea = document.getElementById('chatArea');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const typingIndicator = document.getElementById('typingIndicator');

    function getTimestamp() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function appendMessage(msg, isUser = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isUser ? 'user-msg' : 'bot-msg'}`;
        
        // Handle markdown-style links or bold text occasionally sent by bot
        const formattedMsg = msg.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>')
                                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        msgDiv.innerHTML = `
            <div class="bubble">${formattedMsg}</div>
            <span class="timestamp">${getTimestamp()}</span>
        `;
        
        chatArea.appendChild(msgDiv);
        chatArea.scrollTop = chatArea.scrollHeight;
    }

    async function sendMessage(text) {
        if (!text.trim()) return;

        appendMessage(text, true);
        userInput.value = '';
        
        // Show typing indicator
        typingIndicator.style.display = 'flex';
        chatArea.scrollTop = chatArea.scrollHeight;

        try {
            const response = await fetch('/get', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `msg=${encodeURIComponent(text)}`
            });
            
            const data = await response.json();
            
            // Artificial delay for realism
            setTimeout(() => {
                typingIndicator.style.display = 'none';
                appendMessage(data.response);
            }, 800);

        } catch (error) {
            typingIndicator.style.display = 'none';
            appendMessage("I'm having trouble connecting to the server. Please check your connection.");
        }
    }

    sendBtn.addEventListener('click', () => sendMessage(userInput.value));
    
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage(userInput.value);
    });

    window.quickAction = (text) => {
        sendMessage(text);
    };
});
