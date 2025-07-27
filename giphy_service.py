import requests
import os
import random
import logging

class GiphyService:
    """
    Service for fetching GIFs from Giphy API based on emotions
    """
    
    def __init__(self):
        self.api_key = os.environ.get("GIPHY_API_KEY", "demo_api_key")
        self.base_url = "https://api.giphy.com/v1/gifs"
        
        # Content filtering settings
        self.rating = "g"  # Only family-friendly content
        self.limit = 20    # Number of GIFs to fetch for randomization
        
        # Fallback GIFs for when API is unavailable (using Giphy's public GIFs)
        self.fallback_gifs = {
            'happy': 'https://media.giphy.com/media/l0MYC0LajbaPoEADu/giphy.gif',
            'calm': 'https://media.giphy.com/media/3o7TKTDn976rzVgky4/giphy.gif',
            'relaxed': 'https://media.giphy.com/media/l0MYGb8Q5QnhZ4RJm/giphy.gif',
            'connected': 'https://media.giphy.com/media/l0MYRBdnQGRiWC8Fy/giphy.gif',
            'energized': 'https://media.giphy.com/media/l0MYKnSyyXom5PPrO/giphy.gif',
            'clear': 'https://media.giphy.com/media/3o7TKP2ZNeTevHU4r6/giphy.gif',
            'hopeful': 'https://media.giphy.com/media/3o7TKRwpns23QMNNiE/giphy.gif',
            'forgiven': 'https://media.giphy.com/media/l0MYGb8Q5QnhZ4RJm/giphy.gif',
            'positive': 'https://media.giphy.com/media/l0MYC0LajbaPoEADu/giphy.gif',
            'uplifted': 'https://media.giphy.com/media/3o7TKTDn976rzVgky4/giphy.gif'
        }
    
    def get_opposite_emotion_gif(self, opposite_emotion):
        """
        Fetch a GIF that represents the opposite emotion
        
        Args:
            opposite_emotion (str): The opposite emotion to search for
            
        Returns:
            str: URL of the selected GIF
        """
        try:
            # Define search terms for the opposite emotion
            search_terms = self._get_search_terms(opposite_emotion)
            
            # Try to fetch from Giphy API
            gif_url = self._fetch_from_giphy(search_terms)
            
            if gif_url:
                return gif_url
            else:
                # Fallback to predefined GIFs
                return self.fallback_gifs.get(opposite_emotion, self.fallback_gifs['positive'])
                
        except Exception as e:
            logging.error(f"Error fetching GIF: {str(e)}")
            return self.fallback_gifs.get(opposite_emotion, self.fallback_gifs['positive'])
    
    def _fetch_from_giphy(self, search_terms):
        """
        Fetch GIF from Giphy API
        
        Args:
            search_terms (list): List of search terms to try
            
        Returns:
            str: GIF URL or None if failed
        """
        for term in search_terms:
            try:
                url = f"{self.base_url}/search"
                params = {
                    'api_key': self.api_key,
                    'q': term,
                    'limit': self.limit,
                    'rating': self.rating,
                    'lang': 'en'
                }
                
                response = requests.get(url, params=params, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    if data['data']:
                        # Randomly select a GIF from the results
                        gif = random.choice(data['data'])
                        return gif['images']['original']['url']
                        
            except requests.RequestException as e:
                logging.warning(f"Giphy API request failed for term '{term}': {str(e)}")
                continue
        
        return None
    
    def _get_search_terms(self, emotion):
        """
        Get search terms for a specific emotion
        
        Args:
            emotion (str): The emotion to get search terms for
            
        Returns:
            list: List of search terms
        """
        emotion_terms = {
            'happy': ['happy', 'joy', 'smile', 'celebration', 'laughter', 'fun'],
            'calm': ['calm', 'peaceful', 'zen', 'meditation', 'tranquil'],
            'relaxed': ['relaxed', 'chill', 'peaceful', 'breathing', 'zen'],
            'connected': ['friendship', 'love', 'together', 'hug', 'connection'],
            'energized': ['energy', 'excited', 'pumped up', 'motivation', 'power'],
            'clear': ['clarity', 'understanding', 'lightbulb', 'solution', 'eureka'],
            'hopeful': ['hope', 'optimism', 'bright future', 'dreams', 'possibility'],
            'forgiven': ['forgiveness', 'peace', 'self love', 'acceptance'],
            'positive': ['positive', 'good vibes', 'optimism', 'sunshine'],
            'uplifted': ['uplifting', 'inspiration', 'motivation', 'encouragement']
        }
        
        return emotion_terms.get(emotion, ['happy', 'positive', 'good vibes'])
    
    def search_contextual_gif(self, keyword, detected_emotion):
        """
        Search for contextually relevant GIFs using AI-generated keywords
        
        Args:
            keyword (str): AI-generated keyword for GIF search
            detected_emotion (str): The user's detected emotion for context
            
        Returns:
            str: URL of the GIF or fallback GIF
        """
        try:
            logging.info(f"Contextual GIF search: keyword='{keyword}', emotion='{detected_emotion}'")
            
            # Search for GIFs with the AI-generated keyword
            url = f"{self.base_url}/search"
            params = {
                'api_key': self.api_key,
                'q': keyword,
                'limit': 15,
                'rating': 'g',
                'lang': 'en'
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('data'):
                    # Get a random GIF from results
                    gif = random.choice(data['data'])
                    gif_url = gif['images']['original']['url']
                    logging.info(f"Found contextual GIF: {gif_url}")
                    return gif_url
            
            # Fallback search with emotion-specific terms
            return self.get_emotion_appropriate_gif(detected_emotion)
            
        except Exception as e:
            logging.error(f"Error fetching contextual GIF: {str(e)}")
            return self.get_emotion_appropriate_gif(detected_emotion)
    
    def get_emotion_appropriate_gif(self, emotion):
        """
        Get an appropriate GIF based on detected emotion with smart fallbacks
        
        Args:
            emotion (str): The detected emotion
            
        Returns:
            str: URL of the GIF
        """
        try:
            # Emotion-specific search terms that actually help
            emotion_gifs = {
                'sad': ['cute animals', 'funny cats', 'heartwarming', 'comfort', 'virtual hug'],
                'angry': ['zen', 'peaceful nature', 'calming', 'breathe', 'meditation'],
                'anxious': ['calm', 'peaceful', 'breathe slowly', 'relaxing', 'gentle'],
                'lonely': ['friendship', 'community', 'love', 'connection', 'support'],
                'tired': ['rest', 'cozy', 'peaceful sleep', 'gentle', 'comfort'],
                'confused': ['clarity', 'lightbulb moment', 'understanding', 'clear path'],
                'frustrated': ['zen', 'patience', 'calm down', 'peace'],
                'worried': ['reassuring', 'its okay', 'calm', 'support'],
                'stressed': ['relax', 'breathe', 'peaceful', 'zen garden'],
                'disappointed': ['hope', 'tomorrow', 'new beginnings', 'encouragement'],
                'overwhelmed': ['one step', 'slow down', 'breathe', 'simple'],
                'hurt': ['healing', 'comfort', 'gentle care', 'recovery'],
                'fearful': ['brave', 'courage', 'strong', 'you got this'],
                'rejected': ['self love', 'worth', 'acceptance', 'valuable'],
                'guilty': ['forgiveness', 'its okay', 'move forward', 'self compassion'],
                'helpless': ['strength', 'you can do it', 'empowerment', 'capable']
            }
            
            # Get appropriate search terms
            search_terms = emotion_gifs.get(emotion.lower(), ['uplifting', 'positive', 'smile'])
            selected_term = random.choice(search_terms)
            
            url = f"{self.base_url}/search"
            params = {
                'api_key': self.api_key,
                'q': selected_term,
                'limit': 15,
                'rating': 'g',
                'lang': 'en'
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('data'):
                    gif = random.choice(data['data'])
                    return gif['images']['original']['url']
            
            return self.fallback_gifs.get('positive', 'https://media.giphy.com/media/l0MYC0LajbaPoEADu/giphy.gif')
            
        except Exception as e:
            logging.error(f"Error in emotion-appropriate GIF: {str(e)}")
            return self.fallback_gifs.get('positive', 'https://media.giphy.com/media/l0MYC0LajbaPoEADu/giphy.gif')

    def validate_gif_url(self, url):
        """
        Validate that a GIF URL is accessible
        
        Args:
            url (str): The GIF URL to validate
            
        Returns:
            bool: True if URL is valid and accessible
        """
        try:
            response = requests.head(url, timeout=3)
            return response.status_code == 200
        except:
            return False
