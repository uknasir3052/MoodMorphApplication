class ChatInterface {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.chatMessages = document.getElementById('chatMessages');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.charCount = document.getElementById('charCount');
        
        this.messageHistory = this.loadChatHistory();
        this.isProcessing = false;
        
        this.initializeEventListeners();
        this.displayChatHistory();
        this.autoResizeTextarea();
    }
    
    initializeEventListeners() {
        // Send button click
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Enter key to send (Shift+Enter for new line)
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Character count and auto-resize
        this.messageInput.addEventListener('input', () => {
            this.updateCharCount();
            this.autoResizeTextarea();
        });
        
        // Focus on input when page loads
        this.messageInput.focus();
    }
    
    updateCharCount() {
        const length = this.messageInput.value.length;
        this.charCount.textContent = length;
        
        // Update character count styling
        if (length > 450) {
            this.charCount.classList.add('char-danger');
            this.charCount.classList.remove('char-warning');
        } else if (length > 400) {
            this.charCount.classList.add('char-warning');
            this.charCount.classList.remove('char-danger');
        } else {
            this.charCount.classList.remove('char-warning', 'char-danger');
        }
    }
    
    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message || this.isProcessing) return;
        
        this.isProcessing = true;
        this.updateSendButton(true);
        
        // Add user message to chat
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.updateCharCount();
        this.autoResizeTextarea();
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send message to backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            if (data.success) {
                // Add bot response
                this.addMessage(data.response, 'bot');
                
                // Add GIF if available
                if (data.gif_url) {
                    this.addGifMessage(data.gif_url);
                }
            } else {
                this.addMessage("I'm having trouble right now, but I'm still here for you. Can you try telling me again?", 'bot');
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.addMessage("Something's not working quite right on my end, but don't worry - I'm still listening. Try again?", 'bot');
        } finally {
            this.isProcessing = false;
            this.updateSendButton(false);
            this.messageInput.focus();
        }
    }
    
    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = `<p>${this.escapeHtml(text)}</p>`;
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = this.formatTime(new Date());
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Save to history
        this.messageHistory.push({
            text: text,
            sender: sender,
            timestamp: new Date().toISOString()
        });
        this.saveChatHistory();
        
        // Add animation class
        messageDiv.classList.add('message-sent');
        setTimeout(() => messageDiv.classList.remove('message-sent'), 300);
    }
    
    addGifMessage(gifUrl) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message gif-message';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const img = document.createElement('img');
        img.src = gifUrl;
        img.alt = 'Mood-boosting GIF';
        img.style.maxWidth = '100%';
        img.style.borderRadius = '0.75rem';
        img.onload = () => this.scrollToBottom();
        
        contentDiv.appendChild(img);
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = this.formatTime(new Date());
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Save to history
        this.messageHistory.push({
            text: `[GIF: ${gifUrl}]`,
            sender: 'bot',
            timestamp: new Date().toISOString(),
            isGif: true,
            gifUrl: gifUrl
        });
        this.saveChatHistory();
    }
    
    showTypingIndicator() {
        this.typingIndicator.style.display = 'block';
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }
    
    updateSendButton(isLoading) {
        this.sendBtn.disabled = isLoading;
        if (isLoading) {
            this.sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            this.sendBtn.classList.add('sending');
        } else {
            this.sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';
            this.sendBtn.classList.remove('sending');
        }
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
    
    formatTime(date) {
        return date.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true 
        });
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Chat history management
    loadChatHistory() {
        try {
            const saved = localStorage.getItem('moodmorph_chat_history');
            return saved ? JSON.parse(saved) : [];
        } catch (error) {
            console.error('Error loading chat history:', error);
            return [];
        }
    }
    
    saveChatHistory() {
        try {
            // Keep only last 50 messages
            const recentHistory = this.messageHistory.slice(-50);
            localStorage.setItem('moodmorph_chat_history', JSON.stringify(recentHistory));
        } catch (error) {
            console.error('Error saving chat history:', error);
        }
    }
    
    displayChatHistory() {
        // Clear existing messages except the welcome message
        const welcomeMessage = this.chatMessages.querySelector('.message');
        this.chatMessages.innerHTML = '';
        this.chatMessages.appendChild(welcomeMessage);
        
        // Display recent history (last 10 messages)
        const recentMessages = this.messageHistory.slice(-10);
        recentMessages.forEach(msg => {
            if (msg.isGif) {
                this.addGifMessageFromHistory(msg.gifUrl, msg.timestamp);
            } else {
                this.addMessageFromHistory(msg.text, msg.sender, msg.timestamp);
            }
        });
        
        this.scrollToBottom();
    }
    
    addMessageFromHistory(text, sender, timestamp) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = `<p>${this.escapeHtml(text)}</p>`;
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = this.formatTime(new Date(timestamp));
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        
        this.chatMessages.appendChild(messageDiv);
    }
    
    addGifMessageFromHistory(gifUrl, timestamp) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message gif-message';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const img = document.createElement('img');
        img.src = gifUrl;
        img.alt = 'Mood-boosting GIF';
        img.style.maxWidth = '100%';
        img.style.borderRadius = '0.75rem';
        
        contentDiv.appendChild(img);
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = this.formatTime(new Date(timestamp));
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        
        this.chatMessages.appendChild(messageDiv);
    }
    
    clearHistory() {
        this.messageHistory = [];
        localStorage.removeItem('moodmorph_chat_history');
        
        // Reset to welcome message only
        this.chatMessages.innerHTML = `
            <div class="message bot-message">
                <div class="message-content">
                    <p>Hello! I'm MoodMorph, your AI assistant. I'm here to help brighten your day and assist with any questions you might have. How are you feeling today? 🌟</p>
                </div>
                <div class="message-time">05:13 AM</div>
            </div>
        `;
    }
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chatInterface = new ChatInterface();
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K to clear chat
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        if (confirm('Clear chat history?')) {
            window.chatInterface.clearHistory();
        }
    }
});