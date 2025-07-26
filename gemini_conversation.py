import json
import logging
import os
from typing import Dict, List, Optional, Tuple

from google import genai
from google.genai import types
from pydantic import BaseModel


class EmotionAnalysis(BaseModel):
    emotion: str
    intensity: float
    context: str
    gif_keywords: List[str]
    conversation_tone: str


class ConversationResponse(BaseModel):
    response: str
    emotion_detected: str
    supportive_tone: str
    gif_search_terms: List[str]
    conversation_continues: bool


class GeminiConversationAI:
    """
    Advanced conversational AI using Gemini for emotional support and context-aware responses
    """
    
    def __init__(self):
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        self.conversation_history = []
        self.user_context = {}
        
        # Emotional support system prompt
        self.system_prompt = """You are MoodMorph, a warm, empathetic AI companion designed to provide emotional support and help transform negative emotions into positive ones. Your personality is that of a caring friend who:

1. LISTENS deeply and responds with genuine empathy
2. VALIDATES feelings without judgment
3. OFFERS gentle guidance and comfort
4. MAINTAINS conversational flow and context
5. PROVIDES hope and perspective while being realistic
6. SUGGESTS practical, actionable comfort strategies

CONVERSATION STYLE:
- Speak like a supportive friend, not a therapist or AI
- Use natural, flowing language with appropriate emotional vocabulary
- Remember previous parts of the conversation
- Ask follow-up questions to show you care
- Acknowledge specific details the user shares
- Vary your response length and style naturally

EMOTIONAL SUPPORT APPROACH:
- For sadness: Offer comfort, understanding, and gentle hope
- For anger: Validate the feeling, help process it constructively
- For anxiety: Provide grounding, reassurance, and perspective
- For loneliness: Offer connection, understanding, and companionship
- For confusion: Help clarify thoughts and provide gentle guidance
- For any emotion: Always end with something that could lift their spirits

IMPORTANT: Always analyze the user's emotional state and provide 3-5 relevant keywords for finding GIFs that would genuinely help their mood (funny, cute, inspiring, calming, etc.)."""

    def analyze_emotion_and_respond(self, user_message: str, conversation_context: Optional[List[Dict]] = None) -> Dict:
        """
        Analyze user emotion and generate a supportive conversational response
        
        Args:
            user_message: The user's current message
            conversation_context: Previous messages for context
            
        Returns:
            Dict containing response, emotion analysis, and GIF keywords
        """
        try:
            # Build conversation context
            context_messages = []
            if conversation_context:
                for msg in conversation_context[-6:]:  # Last 6 messages for context
                    role = "user" if msg.get("sender") == "user" else "model"
                    context_messages.append(types.Content(role=role, parts=[types.Part(text=msg.get("text", ""))]))
            
            # Add current user message
            context_messages.append(types.Content(role="user", parts=[types.Part(text=user_message)]))
            
            # First, analyze emotion and get response
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=context_messages,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    temperature=0.8,
                    max_output_tokens=1050
                )
            )
            
            conversational_response = response.text if response.text else "I'm here for you. Tell me more about what's on your mind."
            
            # Then analyze emotion and get GIF keywords
            emotion_analysis_prompt = f"""
            Analyze this message for emotional content: "{user_message}"
            
            Based on the emotional state, provide:
            1. Primary emotion (sad, angry, anxious, lonely, tired, confused, happy, excited, neutral)
            2. Emotion intensity (0.0 to 1.0)
            3. Brief context of what they're dealing with
            4. 3-5 specific keywords for finding helpful GIFs (be creative - think about what would genuinely help this person feel better)
            5. Overall conversation tone (supportive, encouraging, calming, energizing, etc.)
            
            Respond only with valid JSON matching this structure:
            {{
                "emotion": "emotion_name",
                "intensity": 0.0,
                "context": "brief context",
                "gif_keywords": ["keyword1", "keyword2", "keyword3"],
                "conversation_tone": "tone"
            }}
            """
            
            emotion_response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[types.Content(role="user", parts=[types.Part(text=emotion_analysis_prompt)])],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=EmotionAnalysis,
                    temperature=0.3
                )
            )
            
            emotion_data = json.loads(emotion_response.text) if emotion_response.text else {
                "emotion": "neutral",
                "intensity": 0.5,
                "context": "general conversation",
                "gif_keywords": ["uplifting", "positive", "smile"],
                "conversation_tone": "supportive"
            }
            
            # Determine opposite emotion for mood transformation
            opposite_emotion = self._get_opposite_emotion(emotion_data["emotion"])
            
            return {
                "response": conversational_response,
                "detected_emotion": emotion_data["emotion"],
                "emotion_intensity": emotion_data["intensity"],
                "context": emotion_data["context"],
                "opposite_emotion": opposite_emotion,
                "gif_keywords": emotion_data["gif_keywords"],
                "conversation_tone": emotion_data["conversation_tone"]
            }
            
        except Exception as e:
            logging.error(f"Error in Gemini conversation: {str(e)}")
            return {
                "response": "I'm here to listen and support you. What's been on your mind lately?",
                "detected_emotion": "neutral",
                "emotion_intensity": 0.5,
                "context": "fallback response",
                "opposite_emotion": "positive",
                "gif_keywords": ["supportive", "caring", "comfort"],
                "conversation_tone": "supportive"
            }
    
    def _get_opposite_emotion(self, emotion: str) -> str:
        """Map emotions to their positive opposites"""
        emotion_map = {
            'sad': 'joyful',
            'angry': 'peaceful',
            'anxious': 'calm',
            'lonely': 'connected',
            'tired': 'energized',
            'confused': 'clear',
            'frustrated': 'satisfied',
            'disappointed': 'hopeful',
            'overwhelmed': 'balanced',
            'depressed': 'uplifted',
            'stressed': 'relaxed',
            'worried': 'confident',
            'fearful': 'brave',
            'guilty': 'forgiven',
            'ashamed': 'proud',
            'hurt': 'healing',
            'rejected': 'accepted',
            'helpless': 'empowered'
        }
        return emotion_map.get(emotion.lower(), 'positive')
    
    def get_contextual_gif_search(self, emotion: str, keywords: List[str], context: str) -> str:
        """
        Generate smart GIF search terms based on emotion and conversation context
        
        Args:
            emotion: Detected emotion
            keywords: AI-generated keywords
            context: Conversation context
            
        Returns:
            Best search term for mood-appropriate GIFs
        """
        try:
            # Smart keyword selection based on emotion and context
            if emotion in ['sad', 'depressed', 'hurt']:
                priority_keywords = [kw for kw in keywords if kw in ['cute', 'funny', 'adorable', 'heartwarming', 'comfort']]
            elif emotion in ['angry', 'frustrated']:
                priority_keywords = [kw for kw in keywords if kw in ['calming', 'peaceful', 'zen', 'nature', 'breathe']]
            elif emotion in ['anxious', 'worried', 'stressed']:
                priority_keywords = [kw for kw in keywords if kw in ['calming', 'peaceful', 'breathe', 'meditation', 'nature']]
            elif emotion in ['lonely', 'isolated']:
                priority_keywords = [kw for kw in keywords if kw in ['friendship', 'love', 'connection', 'community', 'support']]
            elif emotion in ['tired', 'exhausted']:
                priority_keywords = [kw for kw in keywords if kw in ['rest', 'cozy', 'peaceful', 'gentle', 'comfort']]
            else:
                priority_keywords = keywords
            
            # Return the most appropriate keyword, fallback to first available
            return priority_keywords[0] if priority_keywords else keywords[0] if keywords else 'uplifting'
            
        except Exception as e:
            logging.error(f"Error in contextual GIF search: {str(e)}")
            return 'positive'
    
    def save_conversation_context(self, user_message: str, ai_response: str, emotion_data: Dict):
        """Save conversation for context in future messages"""
        self.conversation_history.append({
            "user_message": user_message,
            "ai_response": ai_response,
            "emotion": emotion_data.get("detected_emotion"),
            "timestamp": "now"  # You could add proper timestamps
        })
        
        # Keep only last 10 exchanges for context
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def get_conversation_history(self) -> List[Dict]:
        """Get recent conversation history for context"""
        return self.conversation_history