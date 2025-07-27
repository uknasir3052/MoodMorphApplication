from flask import render_template, request, jsonify, flash, redirect, url_for, session
from app import app, db
from models import EmotionRecord, ContentTemplate
from gemini_conversation import GeminiConversationAI
from giphy_service import GiphyService
import logging

# Initialize services
conversation_ai = GeminiConversationAI()
giphy_service = GiphyService()

@app.route('/')
def index():
    """Main page of the MoodMorph application"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Process chat message using Gemini AI for natural conversation and mood transformation
    """
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_input = data['message'].strip()
        if not user_input:
            return jsonify({'error': 'Empty message provided'}), 400
        
        # Get conversation context from session
        conversation_context = session.get('conversation_context', [])
        
        # Use Gemini AI for emotion analysis and natural response generation
        ai_result = conversation_ai.analyze_emotion_and_respond(user_input, conversation_context)
        
        detected_emotion = ai_result['detected_emotion']
        emotion_intensity = ai_result['emotion_intensity']
        opposite_emotion = ai_result['opposite_emotion']
        gif_keywords = ai_result['gif_keywords']
        ai_response = ai_result['response']
        
        # Get contextually relevant GIF using AI-generated keywords
        best_gif_keyword = conversation_ai.get_contextual_gif_search(
            detected_emotion, gif_keywords, ai_result['context']
        )
        gif_url = giphy_service.search_contextual_gif(best_gif_keyword, detected_emotion)
        
        # Store conversation context in session for continuity
        conversation_context.append({
            'sender': 'user',
            'text': user_input,
            'timestamp': 'now'
        })
        conversation_context.append({
            'sender': 'bot',
            'text': ai_response,
            'timestamp': 'now'
        })
        
        # Keep only last 10 messages for context
        if len(conversation_context) > 10:
            conversation_context = conversation_context[-10:]
        
        session['conversation_context'] = conversation_context
        
        # Store in database
        record = EmotionRecord(
            user_input=user_input,
            detected_emotion=detected_emotion,
            sentiment_score=emotion_intensity,
            opposite_emotion=opposite_emotion,
            gif_url=gif_url,
            therapeutic_tool=f"Gemini AI: {ai_result['conversation_tone']}"
        )
        db.session.add(record)
        db.session.commit()
        
        # Save conversation context in AI memory
        conversation_ai.save_conversation_context(user_input, ai_response, ai_result)
        
        response = {
            'success': True,
            'response': ai_response,
            'detected_emotion': detected_emotion,
            'emotion_intensity': emotion_intensity,
            'opposite_emotion': opposite_emotion,
            'gif_url': gif_url,
            'gif_keywords': gif_keywords,
            'conversation_tone': ai_result['conversation_tone'],
            'context': ai_result['context']
        }
        
        logging.info(f"Gemini AI analysis: {detected_emotion} -> {opposite_emotion} (intensity: {emotion_intensity})")
        logging.info(f"GIF keywords: {gif_keywords}, selected: {best_gif_keyword}")
        
        return jsonify(response)
        
    except Exception as e:
        logging.error(f"Error in Gemini chat: {str(e)}")
        return jsonify({
            'success': False,
            'response': "I'm here for you, and I want to help. Could you try sharing that with me again?",
            'error': str(e)
        }), 500

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """
    Retrieve suggestions based on recent conversation
    """
    try:
        # Simple suggestions without therapeutic_tools dependency
        suggestions = [
            {'category': 'Movement', 'suggestions': ['Take a 5-minute walk', 'Do gentle stretching', 'Dance to music']},
            {'category': 'Mindfulness', 'suggestions': ['Practice deep breathing', 'Focus on the present', 'Use grounding techniques']},
            {'category': 'Self-Care', 'suggestions': ['Stay hydrated', 'Take a warm shower', 'Rest when needed']}
        ]
        
        breathing_exercises = [
            {'name': '4-7-8 Breathing', 'description': 'Inhale for 4, hold for 7, exhale for 8'},
            {'name': 'Box Breathing', 'description': 'Inhale, hold, exhale, hold - each for 4 counts'}
        ]
        
        return jsonify({
            'suggestions': suggestions,
            'breathing_exercises': breathing_exercises
        })
    except Exception as e:
        logging.error(f"Error in get_suggestions: {str(e)}")
        return jsonify({'error': 'Unable to retrieve suggestions'}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """
    Get recent emotion records
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        records = EmotionRecord.query.order_by(EmotionRecord.timestamp.desc()).limit(limit).all()
        return jsonify([record.to_dict() for record in records])
    except Exception as e:
        logging.error(f"Error in get_history: {str(e)}")
        return jsonify({'error': 'Unable to retrieve history'}), 500

@app.route('/api/upload', methods=['POST'])
def upload_custom_content():
    """
    Handle custom image uploads (for future use)
    """
    return jsonify({'message': 'Custom upload feature coming soon!'}), 501

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500
