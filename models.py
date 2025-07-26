from app import db
from datetime import datetime

class EmotionRecord(db.Model):
    """Model to store user emotion records and interactions"""
    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.Text, nullable=False)
    detected_emotion = db.Column(db.String(50), nullable=False)
    sentiment_score = db.Column(db.Float)
    opposite_emotion = db.Column(db.String(50), nullable=False)
    gif_url = db.Column(db.String(500))
    therapeutic_tool = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, user_input, detected_emotion, sentiment_score, opposite_emotion, gif_url=None, therapeutic_tool=None):
        self.user_input = user_input
        self.detected_emotion = detected_emotion
        self.sentiment_score = sentiment_score
        self.opposite_emotion = opposite_emotion
        self.gif_url = gif_url
        self.therapeutic_tool = therapeutic_tool
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_input': self.user_input,
            'detected_emotion': self.detected_emotion,
            'sentiment_score': self.sentiment_score,
            'opposite_emotion': self.opposite_emotion,
            'gif_url': self.gif_url,
            'therapeutic_tool': self.therapeutic_tool,
            'timestamp': self.timestamp.isoformat()
        }

class ContentTemplate(db.Model):
    """Model to store content templates for different emotions"""
    id = db.Column(db.Integer, primary_key=True)
    emotion = db.Column(db.String(50), nullable=False)
    template_type = db.Column(db.String(50), nullable=False)  # 'therapeutic', 'message', etc.
    content = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'emotion': self.emotion,
            'template_type': self.template_type,
            'content': self.content,
            'is_active': self.is_active
        }
