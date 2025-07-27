// MoodMorph Chat Application

class MoodMorphChat {
    constructor() {
        this.isTyping = false;
        this.messageHistory = [];
        
        this.initializeElements();
        this.bindEvents();
        this.loadChatHistory();
    }
    
    initializeElements() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.charCount = document.getElementById('charCount');
    }
    
    bindEvents() {
        // Send message on button click
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Send message on Enter key (but not Shift+Enter)
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Update character count
        this.messageInput.addEventListener('input', () => this.updateCharCount());
        
        // Focus input on load
        this.messageInput.focus();
    }
    
    updateCharCount() {
        const length = this.messageInput.value.length;
        this.charCount.textContent = length;
        
        // Update styling
        this.charCount.className = '';
        if (length > 450) {
            this.charCount.classList.add('char-danger');
        } else if (length > 400) {
            this.charCount.classList.add('char-warning');
        }
        
        // Enable/disable send button
        this.sendBtn.disabled = length === 0 || length > 500 || this.isTyping;
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isTyping) return;
        
        // Add user message
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.updateCharCount();
        
        // Show typing indicator
        this.showTyping();
        
        try {
            // Send to backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error('Failed to get response');
            }
            
            const data = await response.json();
            
            // Hide typing indicator
            this.hideTyping();
            
            // Add bot response with delay for natural feel
            setTimeout(() => {
                this.addBotResponse(data);
            }, 500);
            
        } catch (error) {
            this.hideTyping();
            this.addMessage("Sorry, I'm having trouble connecting right now. Please try again!", 'bot', true);
            console.error('Error:', error);
        }
    }
    
    addMessage(content, sender, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        if (isError) {
            messageDiv.classList.add('error-message');
        }
        
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${this.escapeHtml(content)}</p>
            </div>
            <div class="message-time">${timeString}</div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Store in history
        this.messageHistory.push({
            content,
            sender,
            timestamp: now.toISOString()
        });
        
        // Save to localStorage
        this.saveChatHistory();
    }
    
    addBotResponse(data) {
        // Add text response
        if (data.response) {
            this.addMessage(data.response, 'bot');
        }
        
        // Add GIF if available
        if (data.gif_url) {
            setTimeout(() => {
                this.addGifMessage(data.gif_url, data.opposite_emotion);
            }, 800);
        }
        
        // Add therapeutic suggestion if available
        if (data.therapeutic_suggestion) {
            setTimeout(() => {
                this.addMessage(data.therapeutic_suggestion, 'bot');
            }, 1200);
        }
    }
    
    addGifMessage(gifUrl, emotion) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message gif-message';
        
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <img src="${gifUrl}" alt="${emotion} GIF" loading="lazy">
            </div>
            <div class="message-time">${timeString}</div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    showTyping() {
        this.isTyping = true;
        this.typingIndicator.style.display = 'block';
        this.sendBtn.disabled = true;
        this.scrollToBottom();
    }
    
    hideTyping() {
        this.isTyping = false;
        this.typingIndicator.style.display = 'none';
        this.updateCharCount();
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    saveChatHistory() {
        // Keep only last 50 messages
        const recentHistory = this.messageHistory.slice(-50);
        localStorage.setItem('moodmorph_chat_history', JSON.stringify(recentHistory));
    }
    
    loadChatHistory() {
        try {
            const saved = localStorage.getItem('moodmorph_chat_history');
            if (saved) {
                this.messageHistory = JSON.parse(saved);
                
                // Restore recent messages (last 10)
                const recentMessages = this.messageHistory.slice(-10);
                recentMessages.forEach(msg => {
                    if (msg.sender === 'user') {
                        this.addMessage(msg.content, msg.sender);
                    } else {
                        this.addMessage(msg.content, msg.sender);
                    }
                });
                
                // Clear the initial welcome message if we have history
                if (recentMessages.length > 0) {
                    const welcomeMsg = this.chatMessages.querySelector('.message');
                    if (welcomeMsg) welcomeMsg.remove();
                }
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
        }
    }
    
    clearHistory() {
        this.messageHistory = [];
        localStorage.removeItem('moodmorph_chat_history');
        this.chatMessages.innerHTML = `
            <div class="message bot-message">
                <div class="message-content">
                    <p>Hey! I'm so glad you're here. Whatever's going on in your world right now, I'm here to listen and help brighten your day. What's on your heart today?</p>
                </div>
                <div class="message-time">Just now</div>
            </div>
        `;
    }
}

// Add some utility functions for better UX
function addSystemMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message system-message';
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <p>${text}</p>
        </div>
    `;
    
    document.getElementById('chatMessages').appendChild(messageDiv);
}

// Initialize chat when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.moodMorphChat = new MoodMorphChat();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (!document.hidden && window.moodMorphChat) {
        // Focus input when user returns to page
        window.moodMorphChat.messageInput.focus();
    }
});

// Handle connection status
window.addEventListener('online', () => {
    addSystemMessage('Connection restored');
});

window.addEventListener('offline', () => {
    addSystemMessage('Connection lost - messages will be sent when back online');
});