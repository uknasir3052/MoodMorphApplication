from textblob import TextBlob
import re
import logging

class EmotionAnalyzer:
    """
    Emotion detection and analysis using TextBlob and keyword matching
    """
    
    def __init__(self):
        # Define emotion keywords and their opposites
        self.emotion_keywords = {
            'sad': ['sad', 'depressed', 'down', 'blue', 'melancholy', 'gloomy', 'dejected', 'miserable'],
            'angry': ['angry', 'mad', 'furious', 'rage', 'irritated', 'annoyed', 'frustrated', 'enraged'],
            'anxious': ['anxious', 'worried', 'nervous', 'stressed', 'panic', 'fear', 'scared', 'overwhelmed'],
            'lonely': ['lonely', 'isolated', 'alone', 'abandoned', 'rejected', 'excluded'],
            'tired': ['tired', 'exhausted', 'drained', 'weary', 'fatigued', 'worn out'],
            'confused': ['confused', 'lost', 'uncertain', 'puzzled', 'bewildered', 'perplexed'],
            'disappointed': ['disappointed', 'let down', 'discouraged', 'disillusioned'],
            'guilty': ['guilty', 'ashamed', 'regretful', 'remorseful']
        }
        
        # Define opposite emotions for transformation
        self.opposite_emotions = {
            'sad': 'happy',
            'angry': 'calm',
            'anxious': 'relaxed',
            'lonely': 'connected',
            'tired': 'energized',
            'confused': 'clear',
            'disappointed': 'hopeful',
            'guilty': 'forgiven',
            'negative': 'positive',
            'neutral': 'uplifted'
        }
        
        # Giphy search terms for opposite emotions
        self.giphy_terms = {
            'happy': ['happy', 'joy', 'celebration', 'smile', 'laughter', 'fun'],
            'calm': ['calm', 'peaceful', 'zen', 'meditation', 'tranquil', 'serene'],
            'relaxed': ['relaxed', 'chill', 'peaceful', 'zen', 'breathing'],
            'connected': ['friendship', 'love', 'together', 'connection', 'hug'],
            'energized': ['energy', 'power', 'motivation', 'excited', 'pumped up'],
            'clear': ['clarity', 'understanding', 'lightbulb', 'eureka', 'solution'],
            'hopeful': ['hope', 'optimism', 'bright future', 'possibility', 'dreams'],
            'forgiven': ['forgiveness', 'peace', 'self love', 'acceptance', 'healing'],
            'positive': ['positive', 'good vibes', 'optimism', 'sunshine', 'rainbow'],
            'uplifted': ['uplifting', 'inspiration', 'motivation', 'encouragement']
        }
    
    def analyze(self, text):
        """
        Analyze the emotional content of the text
        
        Args:
            text (str): The user input text
            
        Returns:
            dict: Analysis results including emotion, sentiment score, and opposite emotion
        """
        try:
            # Clean and preprocess text
            cleaned_text = self._preprocess_text(text)
            
            # Use TextBlob for sentiment analysis
            blob = TextBlob(cleaned_text)
            sentiment_score = blob.sentiment.polarity
            
            # Detect specific emotion through keyword matching
            detected_emotion = self._detect_emotion_keywords(cleaned_text)
            
            # If no specific emotion detected, use sentiment to determine general emotion
            if detected_emotion == 'neutral':
                if sentiment_score < -0.1:
                    detected_emotion = 'negative'
                elif sentiment_score > 0.1:
                    detected_emotion = 'positive'
            
            # Get opposite emotion
            opposite_emotion = self.opposite_emotions.get(detected_emotion, 'positive')
            
            logging.info(f"Emotion analysis: {detected_emotion} -> {opposite_emotion} (sentiment: {sentiment_score})")
            
            return {
                'emotion': detected_emotion,
                'sentiment_score': sentiment_score,
                'opposite_emotion': opposite_emotion,
                'confidence': abs(sentiment_score)
            }
            
        except Exception as e:
            logging.error(f"Error in emotion analysis: {str(e)}")
            return {
                'emotion': 'neutral',
                'sentiment_score': 0.0,
                'opposite_emotion': 'positive',
                'confidence': 0.0
            }
    
    def _preprocess_text(self, text):
        """Clean and preprocess the input text"""
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _detect_emotion_keywords(self, text):
        """Detect emotion based on keyword matching"""
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    # Give higher weight to exact matches
                    if f" {keyword} " in f" {text} ":
                        score += 2
                    else:
                        score += 1
            emotion_scores[emotion] = score
        
        # Return the emotion with the highest score
        if emotion_scores and max(emotion_scores.values()) > 0:
            return max(emotion_scores, key=emotion_scores.get)
        
        return 'neutral'
    
    def get_giphy_search_terms(self, emotion):
        """Get appropriate search terms for Giphy API based on emotion"""
        return self.giphy_terms.get(emotion, ['happy', 'positive', 'good vibes'])
