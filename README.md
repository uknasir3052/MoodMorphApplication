MoodMorph - Emotion Transformation Chatbot

**Overview**

MoodMorph is a Flask-based chatbot application that analyzes user emotions through natural conversation and provides mood transformation through opposite-emotion GIFs and therapeutic responses. The application uses a chat interface that feels like messaging with a supportive friend, rather than interacting with an AI. It uses natural language processing to detect emotions and responds with encouraging messages, mood-boosting GIFs from Giphy, and casual therapeutic suggestions.

**User Preferences**
Preferred communication style: Simple, everyday language.

**System Architecture**

The application follows a traditional server-side web architecture with the following layers:

**Frontend**
  **Technology**: HTML5, CSS3, JavaScript [ES6+]
  **Framework**: Bootstrap 5 with dark theme
  **Architecture**: Chat interface resembling messaging apps (WhatsApp/Telegram style)
  **Key Features**: Real-time conversational UI, message bubbles, typing indicators, GIF display in chat

**Backend**
  **Framework**: Flask (Python)
  **Architecture**: RESTful API design with modular service classes
  **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension
  **Session Management**: Flask sessions with configurable secret key

**Database**
  **Default**: SQLite (development)
  **Production Ready**: Configurable via DATABASE_URL environment variable
  **Schema**: Two main tables - EmotionRecord and ContentTemplate

**Key Components**

**Core Services**

1. **EmotionAnalyzer** (`emotion_analyzer.py`)
   - Uses TextBlob for sentiment analysis
   - Keyword-based emotion detection
   - Maps negative emotions to positive opposites
   - Supports 8 primary emotions: sad, angry, anxious, lonely, tired, confused, disappointed, guilty

2. **GiphyService** (`giphy_service.py`)
   - Integrates with Giphy API for emotion-appropriate GIFs
   - Implements fallback GIFs for API failures
   - Content filtering with family-friendly ratings
   - Randomization for varied user experience

3. **TherapeuticTools** (`therapeutic_tools.py`)
   - Provides breathing exercises (4-7-8, Box Breathing, Belly Breathing)
   - Generates encouraging messages
   - Offers emotion-specific therapeutic interventions

**Database Models**

1. **EmotionRecord**
   - Stores user interactions and analysis results
   - Tracks emotion progression over time
   - Links therapeutic tools to specific sessions

2. **ContentTemplate**
   - Manages reusable content for different emotions
   - Supports multiple template types
   - Allows for content activation/deactivation

**API Endpoints**

- `GET /` - Serves the chat interface
- `POST /api/chat` - Processes conversational messages with emotion analysis and response generation
- `GET /api/history` - Retrieves recent chat history
- `GET /api/suggestions` - Retrieves therapeutic suggestions

**Data Flow**

1. **User Input**: User submits emotional text through web interface
2. **Emotion Analysis**: TextBlob analyzes sentiment, keywords identify specific emotions
3. **Content Generation**: System fetches appropriate GIF and therapeutic tool
4. **Database Storage**: Interaction data stored for history and analytics
5. **Response Display**: Frontend displays results with encouraging message

**External Dependencies**

**Required APIs**
  **Giphy API**: For emotion-appropriate GIFs and memes
  - Requires GIPHY_API_KEY environment variable
  - Fallback system for API unavailability

**Python Libraries**
  **Flask**: Web framework and request handling
  **SQLAlchemy**: Database ORM and migrations
  **TextBlob**: Natural language processing and sentiment analysis
  **Requests**: HTTP client for external API calls

**Frontend Dependencies**
  **Bootstrap 5**: UI framework with dark theme
  **Font Awesome**: Icon library
  **Vanilla JavaScript**: Client-side interactions

**Deployment Strategy**

**Environment Configuration**
  **Development**: SQLite database, debug mode enabled
  **Production**: PostgreSQL support via DATABASE_URL
  **Security**: Configurable session secrets, proxy-aware setup

**Required Environment Variables**
  `DATABASE_URL`: Database connection string
  `GIPHY_API_KEY`: Giphy API authentication
  `SESSION_SECRET`: Flask session encryption key

**Hosting Considerations**
  **Platform**: Designed for Replit deployment
  **Scalability**: Stateless design supports horizontal scaling
  **Monitoring**: Built-in logging for debugging and analytics

 **Database Migration**
- Automatic table creation on application startup
- SQLAlchemy migrations for schema changes
- Support for multiple database backends through configuration

The application is designed to be lightweight, user-friendly, and therapeutically beneficial, focusing on transforming negative emotional states through positive visual content and proven therapeutic techniques.
