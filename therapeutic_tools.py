import random
import logging

class TherapeuticTools:
    """
    Provides therapeutic interventions and tools for different emotions
    """
    
    def __init__(self):
        self.breathing_exercises = [
            {
                'name': '4-7-8 Breathing',
                'description': 'Inhale for 4 counts, hold for 7, exhale for 8. Repeat 4 times.',
                'duration': '2-3 minutes',
                'instructions': [
                    'Sit comfortably with your back straight',
                    'Place your tongue against the roof of your mouth behind your teeth',
                    'Exhale completely through your mouth',
                    'Close your mouth and inhale through nose for 4 counts',
                    'Hold your breath for 7 counts',
                    'Exhale through mouth for 8 counts',
                    'Repeat this cycle 4 times'
                ]
            },
            {
                'name': 'Box Breathing',
                'description': 'Inhale, hold, exhale, hold - each for 4 counts.',
                'duration': '3-5 minutes',
                'instructions': [
                    'Sit or lie down comfortably',
                    'Inhale slowly through your nose for 4 counts',
                    'Hold your breath for 4 counts',
                    'Exhale slowly through your mouth for 4 counts',
                    'Hold empty for 4 counts',
                    'Repeat for 10-15 cycles'
                ]
            },
            {
                'name': 'Belly Breathing',
                'description': 'Deep diaphragmatic breathing to activate relaxation response.',
                'duration': '5-10 minutes',
                'instructions': [
                    'Lie down or sit comfortably',
                    'Place one hand on chest, one on belly',
                    'Breathe slowly through your nose',
                    'Feel your belly rise more than your chest',
                    'Exhale slowly through pursed lips',
                    'Continue for 5-10 minutes'
                ]
            }
        ]
        
        self.mindfulness_prompts = [
            {
                'title': '5-4-3-2-1 Grounding',
                'description': 'Notice 5 things you see, 4 things you can touch, 3 things you hear, 2 things you smell, 1 thing you taste.',
                'type': 'grounding'
            },
            {
                'title': 'Body Scan',
                'description': 'Starting from your toes, slowly notice each part of your body and any sensations.',
                'type': 'awareness'
            },
            {
                'title': 'Loving Kindness',
                'description': 'Send thoughts of love and kindness to yourself, then to someone you love, then to someone neutral, and finally to someone difficult.',
                'type': 'compassion'
            },
            {
                'title': 'Present Moment',
                'description': 'Focus entirely on what you\'re doing right now. Notice every detail of the current moment.',
                'type': 'presence'
            }
        ]
        
        self.emotion_tools = {
            'sad': {
                'tools': ['gratitude_practice', 'movement', 'social_connection'],
                'messages': [
                    "It's okay to feel sad. This feeling is temporary and will pass.",
                    "Your sadness is valid. Let's find something to lift your spirits.",
                    "Even in difficult moments, there are small things to be grateful for."
                ]
            },
            'angry': {
                'tools': ['breathing_exercise', 'physical_release', 'perspective_shift'],
                'messages': [
                    "Your anger is telling you something important. Let's channel it constructively.",
                    "Take a deep breath. This feeling will pass, and you can handle this.",
                    "It's natural to feel angry sometimes. Let's find a healthy way to process it."
                ]
            },
            'anxious': {
                'tools': ['breathing_exercise', 'grounding', 'reassurance'],
                'messages': [
                    "Anxiety is uncomfortable but not dangerous. You are safe in this moment.",
                    "Focus on what you can control right now. You've overcome challenges before.",
                    "This anxious feeling will pass. Let's ground yourself in the present moment."
                ]
            },
            'lonely': {
                'tools': ['social_connection', 'self_compassion', 'meaningful_activity'],
                'messages': [
                    "Feeling lonely is human. You are worthy of connection and love.",
                    "Even when alone, you are not forgotten. Someone cares about you.",
                    "This loneliness is temporary. You have the strength to reach out when ready."
                ]
            },
            'tired': {
                'tools': ['rest_planning', 'energy_conservation', 'gentle_movement'],
                'messages': [
                    "Your body is asking for rest. It's okay to slow down.",
                    "Tiredness is a sign to be gentle with yourself today.",
                    "Rest is productive. You deserve to recharge."
                ]
            },
            'confused': {
                'tools': ['clarity_exercise', 'step_by_step', 'perspective_gathering'],
                'messages': [
                    "Confusion is the beginning of understanding. You'll find clarity.",
                    "It's okay not to have all the answers right now.",
                    "One step at a time. You don't need to figure everything out today."
                ]
            }
        }
        
        self.general_suggestions = [
            {
                'category': 'Movement',
                'suggestions': [
                    'Take a 5-minute walk outside',
                    'Do gentle stretching',
                    'Dance to your favorite song',
                    'Try some jumping jacks'
                ]
            },
            {
                'category': 'Creative',
                'suggestions': [
                    'Draw or doodle something',
                    'Write in a journal',
                    'Listen to uplifting music',
                    'Take photos of beautiful things around you'
                ]
            },
            {
                'category': 'Social',
                'suggestions': [
                    'Text a friend you haven\'t talked to in a while',
                    'Call someone who makes you laugh',
                    'Write a gratitude note to someone',
                    'Join an online community of interest'
                ]
            },
            {
                'category': 'Self-Care',
                'suggestions': [
                    'Take a warm shower or bath',
                    'Make yourself a nice cup of tea',
                    'Practice good posture',
                    'Hydrate with a glass of water'
                ]
            }
        ]
        
        # Chat response templates for natural conversation
        self.chat_responses = {
            'sad': [
                "Oh, I can really feel that heaviness in what you're sharing. Life can be so tough sometimes, can't it? I'm right here with you through this.",
                "That sounds incredibly hard, and I'm so sorry you're going through this right now. You know what though? You're not alone in feeling this way.",
                "Ugh, those sad feelings can just weigh everything down. I wish I could give you the biggest hug right now. You're being so brave by reaching out.",
                "I hear you, really truly hear you. Sometimes the world just feels too much, doesn't it? But you're here, you're talking about it, and that takes real courage.",
                "Oh sweetie, that sounds so painful. I know it probably feels like this sadness will never lift, but I promise you it will. You've gotten through hard days before."
            ],
            'angry': [
                "Whoa, I can absolutely feel that fire in your words! That must be SO frustrating. Sometimes things just push us past our limit, you know?",
                "Oh man, that would make me furious too! Your anger totally makes sense - when we care about something and it goes wrong, of course we get heated.",
                "I get it, I really do. That burning feeling when everything seems to be going sideways - it's like your whole body is just ready to explode, right?",
                "Ugh, that sounds maddening! You know what though? That anger is telling us something important - it means you give a damn, and that's actually beautiful.",
                "I'm feeling that frustration with you! Sometimes the world just doesn't cooperate with what we need, does it? But we'll figure this out together."
            ],
            'anxious': [
                "Oh honey, I can practically feel those butterflies racing around in your stomach. Anxiety is just the worst, isn't it? But you're going to be okay, I promise.",
                "That anxious spiral is so real - when your mind just won't stop racing and everything feels like it could go wrong. I've been there, and you're not alone.",
                "Oof, anxiety brain is so mean sometimes! It loves to whisper all these scary 'what ifs' that probably won't even happen. Take a deep breath with me?",
                "I can sense that worried energy from here. Your mind is trying to protect you by thinking of every possible problem, but that's exhausting! Let's slow it down together.",
                "That jittery, can't-sit-still feeling is so uncomfortable. I know it feels huge right now, but remember - you've survived 100% of your anxious moments so far."
            ],
            'lonely': [
                "Oh, that ache of loneliness is so real and so hard. Even when there are people around, sometimes we can feel like we're on an island, you know?",
                "Ugh, loneliness hits different, doesn't it? Like this hollow feeling that just sits in your chest. I'm here with you right now though, truly.",
                "That disconnected feeling is so rough. Sometimes even in a crowded room we can feel like no one really sees us. But I see you, and you matter.",
                "I know that empty feeling where it seems like everyone else has their people but you're just... floating. You're not as alone as it feels, I promise.",
                "Oh sweetie, that loneliness can feel so heavy and endless. But reaching out to me right now? That's you fighting against it, and I'm so proud of you."
            ],
            'tired': [
                "Oh honey, you sound absolutely drained. Sometimes tired isn't just sleepy - it's like your soul needs a nap, you know?",
                "I can hear that bone-deep exhaustion in what you're saying. When everything feels like it takes twice the energy it should... ugh, that's so hard.",
                "That kind of tired where even simple things feel overwhelming? I totally get that. You've been running on empty for too long, haven't you?",
                "It sounds like you've been carrying the world on your shoulders. No wonder you're exhausted! You need and deserve some real rest.",
                "That weary feeling when even breathing feels like work... I hear you. Sometimes our bodies and hearts are just begging us to slow down."
            ],
            'confused': [
                "Ugh, that foggy, scattered feeling when nothing makes sense is so frustrating! Like trying to solve a puzzle with half the pieces missing.",
                "I can feel that mental spinning from here - when your brain just can't seem to land on anything solid. It's like everything is swirling around, right?",
                "That lost, 'which way is up' feeling is so disorienting. Sometimes life throws us curveballs and we just need time to find our footing again.",
                "Oh, the overwhelm of not knowing which way to turn! Your mind is probably going a million miles an hour trying to figure it all out.",
                "That unclear, muddy feeling where everything seems complicated and nothing feels certain - I've been there, and it's exhausting for your brain."
            ],
            'positive': [
                "Oh my gosh, I can feel the sunshine in your words! It's so beautiful when life feels light and good like this.",
                "Your happiness is absolutely contagious right now! I'm literally smiling just reading what you shared. Life's treating you well!",
                "I LOVE this energy! There's something so wonderful about those moments when everything just feels right with the world.",
                "This is making my whole day brighter! It's gorgeous when we can feel grateful and joyful about where we are.",
                "Your good vibes are radiating through the screen! These are the moments that make all the tough times worth it, aren't they?"
            ],
            'neutral': [
                "Hey there! Sometimes it's nice to just check in without any big feelings, you know? Just existing in the moment.",
                "I love that you reached out just to share what's going on. Sometimes the ordinary moments need acknowledging too.",
                "Thanks for letting me into your day! Even when things feel pretty neutral, it's good to touch base and just be present.",
                "I'm so glad you're here. Sometimes we don't need to feel anything dramatic - just being and sharing is enough.",
                "It's really nice when we can just chat without any heavy stuff. How's your world treating you today?"
            ]
        }
        
        # Casual therapeutic suggestions that sound like friend advice
        self.casual_suggestions = {
            'sad': [
                "You know what always works for me? Put on that one song that never fails to make you smile - even if you have to fake it at first, sometimes your heart catches up.",
                "Here's a weird one that actually helps: do something tiny and kind for someone else. Like, text a friend a compliment or leave a nice review somewhere. It shifts something inside.",
                "This might sound too simple, but go sit outside for just 5 minutes. Even if it's cold or whatever - sometimes our souls just need sky and air.",
                "What if you called that one person who always makes you laugh? You know, the one who has the ridiculous stories? Sometimes we need to borrow some joy."
            ],
            'angry': [
                "When you're ready, maybe try going for a quick walk or doing some jumping jacks - sometimes we need to move that energy through our body.",
                "I know it sounds simple, but taking some deep breaths can actually help reset your nervous system when you're heated.",
                "Maybe write down exactly what's bothering you - sometimes getting it out of our head and onto paper helps us see it differently.",
                "If you can, try to do something physical - even just stretching can help release some of that tension."
            ],
            'anxious': [
                "Try this: name 5 things you can see, 4 things you can touch, 3 things you can hear. It helps bring you back to the present moment.",
                "When anxiety hits, sometimes our breathing gets shallow. Try breathing in for 4 counts, holding for 4, then out for 4.",
                "Anxiety loves to focus on 'what if' scenarios. What if you asked yourself 'what is' happening right now instead?",
                "Sometimes a warm drink and a few minutes of just being still can help calm an anxious mind."
            ],
            'lonely': [
                "Even if it feels hard, maybe reach out to one person today - even just a simple text to let them know you're thinking of them.",
                "Sometimes when we feel disconnected, doing something creative or meaningful can help us feel more like ourselves.",
                "You could try going somewhere with other people around - even if you don't talk to anyone, just being around others can help.",
                "What if you wrote yourself a kind note? Sometimes we need to be our own friend first."
            ],
            'tired': [
                "It might be time to give yourself permission to rest without feeling guilty about it. Your body is asking for what it needs.",
                "Sometimes 'tired' means we need to say no to a few things. What could you take off your plate this week?",
                "Try doing one small thing that usually brings you joy - sometimes we're tired because we've forgotten to nourish ourselves.",
                "Maybe tonight you could go to bed 30 minutes earlier than usual. Small changes can make a big difference."
            ],
            'confused': [
                "When everything feels unclear, sometimes it helps to write down what you DO know, even if it's just small things.",
                "What if you talked through your thoughts with someone you trust? Sometimes clarity comes through conversation.",
                "Maybe take a step back from trying to figure it all out right now. Sometimes solutions come when we're not forcing them.",
                "Try asking yourself: what would feel good or right in this moment, even if you can't see the big picture?"
            ]
        }
    
    def get_tool_for_emotion(self, emotion):
        """
        Get appropriate therapeutic tool for a specific emotion
        
        Args:
            emotion (str): The detected emotion
            
        Returns:
            dict: Tool information including exercises and techniques
        """
        try:
            if emotion in self.emotion_tools:
                emotion_data = self.emotion_tools[emotion]
                tool_type = random.choice(emotion_data['tools'])
                
                if tool_type == 'breathing_exercise':
                    return {
                        'name': 'Breathing Exercise',
                        'type': 'breathing',
                        'exercise': random.choice(self.breathing_exercises)
                    }
                elif tool_type == 'grounding':
                    grounding_prompts = [p for p in self.mindfulness_prompts if p['type'] == 'grounding']
                    return {
                        'name': 'Grounding Exercise',
                        'type': 'mindfulness',
                        'exercise': random.choice(grounding_prompts) if grounding_prompts else self.mindfulness_prompts[0]
                    }
                else:
                    return {
                        'name': 'Mindfulness Practice',
                        'type': 'mindfulness',
                        'exercise': random.choice(self.mindfulness_prompts)
                    }
            else:
                # Default tool for unrecognized emotions
                return {
                    'name': 'Breathing Exercise',
                    'type': 'breathing',
                    'exercise': random.choice(self.breathing_exercises)
                }
                
        except Exception as e:
            logging.error(f"Error getting therapeutic tool: {str(e)}")
            return {
                'name': 'Simple Breathing',
                'type': 'breathing',
                'exercise': self.breathing_exercises[0]
            }
    
    def get_encouraging_message(self, detected_emotion, opposite_emotion):
        """
        Get an encouraging message based on the detected emotion
        
        Args:
            detected_emotion (str): The emotion that was detected
            opposite_emotion (str): The opposite emotion we're targeting
            
        Returns:
            str: Encouraging message
        """
        if detected_emotion in self.emotion_tools:
            messages = self.emotion_tools[detected_emotion]['messages']
            return random.choice(messages)
        else:
            return f"Every feeling is temporary. Let's shift towards feeling more {opposite_emotion}."
    
    def get_breathing_exercises(self):
        """Get all available breathing exercises"""
        return self.breathing_exercises
    
    def get_mindfulness_prompts(self):
        """Get all available mindfulness prompts"""
        return self.mindfulness_prompts
    
    def get_general_suggestions(self):
        """Get general mood-enhancement suggestions"""
        return self.general_suggestions
    
    def generate_chat_response(self, user_input, detected_emotion, opposite_emotion):
        """
        Generate a natural, conversational response based on the user's emotion
        
        Args:
            user_input (str): The user's original message
            detected_emotion (str): The detected emotion
            opposite_emotion (str): The target opposite emotion
            
        Returns:
            str: A natural, empathetic response
        """
        try:
            # Get appropriate response template
            if detected_emotion in self.chat_responses:
                responses = self.chat_responses[detected_emotion]
            elif detected_emotion == 'negative':
                responses = self.chat_responses['sad']  # Default negative response
            else:
                responses = self.chat_responses['neutral']
            
            # Select a random response
            base_response = random.choice(responses)
            
            # Add a transition that feels natural
            if detected_emotion in ['sad', 'angry', 'anxious', 'lonely', 'tired', 'confused']:
                transition_phrases = [
                    " Hold on, let me find something that might help lift your spirits.",
                    " Wait, I've got just the thing that might make you smile.",
                    " Okay, here's something that always helps me when I feel like this.",
                    " You know what? I have something perfect for this feeling."
                ]
                base_response += random.choice(transition_phrases)
            
            return base_response
            
        except Exception as e:
            logging.error(f"Error generating chat response: {str(e)}")
            return "I hear you, and I'm here to help. Let me find something to brighten your day."
    
    def get_casual_suggestion(self, detected_emotion):
        """
        Get a casual, friend-like therapeutic suggestion
        
        Args:
            detected_emotion (str): The detected emotion
            
        Returns:
            str: A casual suggestion or None
        """
        try:
            if detected_emotion in self.casual_suggestions:
                suggestions = self.casual_suggestions[detected_emotion]
                return random.choice(suggestions)
            return None
            
        except Exception as e:
            logging.error(f"Error getting casual suggestion: {str(e)}")
            return None
