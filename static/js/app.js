// MoodMorph Application JavaScript

class MoodMorphApp {
    constructor() {
        this.currentEmotion = null;
        this.currentOppositeEmotion = null;
        this.isAnalyzing = false;
        
        this.initializeElements();
        this.bindEvents();
        this.loadRecentHistory();
    }
    
    initializeElements() {
        // Input elements
        this.emotionInput = document.getElementById('emotionInput');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.charCount = document.getElementById('charCount');
        
        // Display elements
        this.loadingIndicator = document.getElementById('loadingIndicator');
        this.resultsSection = document.getElementById('resultsSection');
        this.errorMessage = document.getElementById('errorMessage');
        this.errorText = document.getElementById('errorText');
        
        // Results elements
        this.detectedEmotion = document.getElementById('detectedEmotion');
        this.oppositeEmotion = document.getElementById('oppositeEmotion');
        this.sentimentBar = document.getElementById('sentimentBar');
        this.sentimentValue = document.getElementById('sentimentValue');
        this.encouragingMessage = document.getElementById('encouragingMessage');
        this.responseGif = document.getElementById('responseGif');
        this.newGifBtn = document.getElementById('newGifBtn');
        this.therapeuticTool = document.getElementById('therapeuticTool');
        this.recentHistory = document.getElementById('recentHistory');
    }
    
    bindEvents() {
        // Input events
        this.emotionInput.addEventListener('input', () => this.updateCharCount());
        this.emotionInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                this.analyzeEmotion();
            }
        });
        
        // Button events
        this.analyzeBtn.addEventListener('click', () => this.analyzeEmotion());
        this.clearBtn.addEventListener('click', () => this.clearInput());
        this.newGifBtn.addEventListener('click', () => this.getNewGif());
        
        // Prevent double submissions
        this.emotionInput.addEventListener('paste', () => {
            setTimeout(() => this.updateCharCount(), 10);
        });
    }
    
    updateCharCount() {
        const length = this.emotionInput.value.length;
        this.charCount.textContent = length;
        
        // Update styling based on character count
        this.charCount.className = '';
        if (length > 450) {
            this.charCount.classList.add('char-count-danger');
        } else if (length > 400) {
            this.charCount.classList.add('char-count-warning');
        }
        
        // Enable/disable analyze button
        this.analyzeBtn.disabled = length === 0 || length > 500 || this.isAnalyzing;
    }
    
    clearInput() {
        this.emotionInput.value = '';
        this.updateCharCount();
        this.hideResults();
        this.hideError();
        this.emotionInput.focus();
    }
    
    async analyzeEmotion() {
        const text = this.emotionInput.value.trim();
        
        if (!text) {
            this.showError('Please enter some text describing how you feel.');
            return;
        }
        
        if (text.length > 500) {
            this.showError('Please keep your input under 500 characters.');
            return;
        }
        
        this.isAnalyzing = true;
        this.showLoading();
        this.hideError();
        this.hideResults();
        
        try {
            const response = await fetch('/api/emotion', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to analyze emotion');
            }
            
            const data = await response.json();
            this.displayResults(data);
            this.loadRecentHistory(); // Refresh history
            
        } catch (error) {
            console.error('Error analyzing emotion:', error);
            this.showError(error.message || 'Something went wrong. Please try again.');
        } finally {
            this.isAnalyzing = false;
            this.hideLoading();
            this.updateCharCount();
        }
    }
    
    displayResults(data) {
        // Store current data for potential GIF refresh
        this.currentEmotion = data.detected_emotion;
        this.currentOppositeEmotion = data.opposite_emotion;
        
        // Display emotion analysis
        this.detectedEmotion.textContent = this.capitalizeFirst(data.detected_emotion);
        this.detectedEmotion.className = `emotion-badge emotion-${data.detected_emotion}`;
        
        this.oppositeEmotion.textContent = this.capitalizeFirst(data.opposite_emotion);
        this.oppositeEmotion.className = `emotion-badge emotion-${data.opposite_emotion}`;
        
        // Display sentiment score
        this.updateSentimentBar(data.sentiment_score);
        
        // Display encouraging message
        this.encouragingMessage.textContent = data.encouraging_message;
        
        // Display GIF
        if (data.gif_url) {
            this.responseGif.src = data.gif_url;
            this.responseGif.alt = `${data.opposite_emotion} GIF`;
            this.responseGif.style.display = 'block';
        } else {
            this.responseGif.style.display = 'none';
        }
        
        // Display therapeutic tool
        this.displayTherapeuticTool(data.therapeutic_tool);
        
        // Show results
        this.showResults();
    }
    
    updateSentimentBar(score) {
        // Normalize score from -1,1 to 0,100 for progress bar
        const percentage = ((score + 1) / 2) * 100;
        this.sentimentBar.style.width = `${percentage}%`;
        
        // Color based on sentiment
        this.sentimentBar.className = 'progress-bar';
        if (score < -0.3) {
            this.sentimentBar.classList.add('bg-danger');
        } else if (score < -0.1) {
            this.sentimentBar.classList.add('bg-warning');
        } else if (score < 0.1) {
            this.sentimentBar.classList.add('bg-secondary');
        } else if (score < 0.3) {
            this.sentimentBar.classList.add('bg-info');
        } else {
            this.sentimentBar.classList.add('bg-success');
        }
        
        this.sentimentValue.textContent = `${score.toFixed(2)} (${this.getSentimentLabel(score)})`;
    }
    
    getSentimentLabel(score) {
        if (score < -0.5) return 'Very Negative';
        if (score < -0.1) return 'Negative';
        if (score < 0.1) return 'Neutral';
        if (score < 0.5) return 'Positive';
        return 'Very Positive';
    }
    
    displayTherapeuticTool(tool) {
        if (!tool) {
            this.therapeuticTool.innerHTML = '<p class="text-muted">No specific tool available at the moment.</p>';
            return;
        }
        
        let html = `<h6><i class="fas fa-tools me-2"></i>${tool.name}</h6>`;
        
        if (tool.type === 'breathing' && tool.exercise) {
            html += this.renderBreathingExercise(tool.exercise);
        } else if (tool.type === 'mindfulness' && tool.exercise) {
            html += this.renderMindfulnessExercise(tool.exercise);
        } else {
            html += '<p class="text-muted">Practice some deep breathing and mindfulness.</p>';
        }
        
        this.therapeuticTool.innerHTML = html;
    }
    
    renderBreathingExercise(exercise) {
        let html = `
            <div class="therapeutic-exercise">
                <h6>${exercise.name}</h6>
                <p>${exercise.description}</p>
                <p><strong>Duration:</strong> ${exercise.duration}</p>
                <div class="exercise-steps">
        `;
        
        exercise.instructions.forEach(instruction => {
            html += `<div class="exercise-step">${instruction}</div>`;
        });
        
        html += `
                </div>
                <button class="btn btn-outline-primary btn-sm mt-2" onclick="startBreathingTimer('${exercise.name}')">
                    <i class="fas fa-play me-2"></i>Start Exercise
                </button>
            </div>
        `;
        
        return html;
    }
    
    renderMindfulnessExercise(exercise) {
        return `
            <div class="therapeutic-exercise">
                <h6>${exercise.title}</h6>
                <p>${exercise.description}</p>
                <span class="badge bg-info">${exercise.type}</span>
            </div>
        `;
    }
    
    async getNewGif() {
        if (!this.currentOppositeEmotion) return;
        
        this.newGifBtn.disabled = true;
        this.newGifBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
        
        try {
            const response = await fetch('/api/emotion', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    text: `I want to feel ${this.currentOppositeEmotion}`,
                    refresh_gif: true
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                if (data.gif_url) {
                    this.responseGif.src = data.gif_url;
                }
            }
        } catch (error) {
            console.error('Error getting new GIF:', error);
        } finally {
            this.newGifBtn.disabled = false;
            this.newGifBtn.innerHTML = '<i class="fas fa-sync-alt me-2"></i>Get Another GIF';
        }
    }
    
    async loadRecentHistory() {
        try {
            const response = await fetch('/api/history?limit=5');
            if (response.ok) {
                const history = await response.json();
                this.displayHistory(history);
            }
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }
    
    displayHistory(history) {
        if (!history || history.length === 0) {
            this.recentHistory.innerHTML = '<p class="text-muted">Your recent mood transformations will appear here.</p>';
            return;
        }
        
        let html = '';
        history.forEach(record => {
            const timeAgo = this.getTimeAgo(new Date(record.timestamp));
            html += `
                <div class="history-item">
                    <div class="history-emotion">${this.capitalizeFirst(record.detected_emotion)} → ${this.capitalizeFirst(record.opposite_emotion)}</div>
                    <div class="history-time">${timeAgo}</div>
                </div>
            `;
        });
        
        this.recentHistory.innerHTML = html;
    }
    
    getTimeAgo(date) {
        const now = new Date();
        const diff = now - date;
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);
        
        if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
        if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
        return 'Just now';
    }
    
    showLoading() {
        this.loadingIndicator.style.display = 'block';
        this.analyzeBtn.disabled = true;
        this.analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
    }
    
    hideLoading() {
        this.loadingIndicator.style.display = 'none';
        this.analyzeBtn.disabled = false;
        this.analyzeBtn.innerHTML = '<i class="fas fa-magic me-2"></i>Transform My Mood';
    }
    
    showResults() {
        this.resultsSection.style.display = 'block';
    }
    
    hideResults() {
        this.resultsSection.style.display = 'none';
    }
    
    showError(message) {
        this.errorText.textContent = message;
        this.errorMessage.style.display = 'block';
        setTimeout(() => this.hideError(), 5000); // Auto-hide after 5 seconds
    }
    
    hideError() {
        this.errorMessage.style.display = 'none';
    }
    
    capitalizeFirst(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
}

// Global functions for therapeutic tools
function showBreathingExercise() {
    alert('Try the 4-7-8 breathing technique:\n\n1. Inhale for 4 counts\n2. Hold for 7 counts\n3. Exhale for 8 counts\n4. Repeat 4 times');
}

function showMindfulness() {
    alert('5-4-3-2-1 Grounding Technique:\n\nNotice:\n• 5 things you can see\n• 4 things you can touch\n• 3 things you can hear\n• 2 things you can smell\n• 1 thing you can taste');
}

function showGeneralSuggestions() {
    const suggestions = [
        'Take a 5-minute walk outside',
        'Listen to your favorite uplifting song',
        'Write three things you\'re grateful for',
        'Do some gentle stretching',
        'Text a friend you care about'
    ];
    
    const randomSuggestion = suggestions[Math.floor(Math.random() * suggestions.length)];
    alert(`Quick mood booster suggestion:\n\n${randomSuggestion}`);
}

function startBreathingTimer(exerciseName) {
    alert(`Starting ${exerciseName}!\n\nFind a comfortable position and follow the instructions. Take your time and breathe naturally.`);
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.moodMorphApp = new MoodMorphApp();
});

// Handle page visibility for better user experience
document.addEventListener('visibilitychange', () => {
    if (!document.hidden && window.moodMorphApp) {
        // Refresh history when user returns to the page
        window.moodMorphApp.loadRecentHistory();
    }
});
