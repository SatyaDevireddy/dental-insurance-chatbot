# 🌐 Web Application Setup Guide

This guide explains how to run the Dental Insurance Chatbot as a web application with a beautiful UI and modal chat interface.

## 📋 Overview

The web application provides:

- **Home Page**: Beautiful landing page with features, plans, and information
- **Modal Chat**: Floating chat icon that opens a modal chatbot window
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Chat**: Interactive conversation with the AI assistant
- **Session Management**: Maintains conversation history per session
- **Reset Functionality**: Clear conversation and start fresh

## 🏗️ Architecture

### Frontend

- **HTML/CSS/JavaScript**: Pure frontend with no framework dependencies
- **Templates**: Jinja2 templates in `templates/` folder
- **Static Files**: CSS and JS in `static/` folder
- **Modal Design**: Chat appears in a floating modal window

### Backend

- **Flask**: Python web framework for routing and API
- **REST API**: `/api/chat` endpoint for message processing
- **Session Management**: Flask sessions for conversation tracking
- **Chatbot Integration**: Uses existing LangChain agent, MCP tools, and RAG pipeline

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
# Activate your virtual environment
.\.venv\Scripts\Activate.ps1

# Install Flask and Flask-CORS
pip install Flask>=3.0.0 flask-cors>=4.0.0
```

Or install all dependencies:

```powershell
pip install -r requirements.txt
```

### 2. Configuration

Your existing `.env` file is already configured. Optionally add:

```env
# Flask Configuration (optional)
FLASK_PORT=5000
FLASK_DEBUG=False
FLASK_SECRET_KEY=your-secret-key-here
```

### 3. Run the Web Application

```powershell
# Make sure LM Studio is running (if using local LLM)
# Then start the Flask server
python app.py
```

You should see:

```
🚀 Initializing Dental Insurance Chatbot Web Application...
✅ Sample data loaded
✅ MCP tools initialized
✅ MetLife FEDVIP 2025 plan loaded
✅ MetLife VADIP 2025 plan loaded
✅ Chatbot initialized
🌐 Web application ready!

🌐 Starting web server on http://localhost:5000
📱 Open your browser and navigate to the URL above
💬 Click the chat icon to start chatting!
```

### 4. Open in Browser

Navigate to: **http://localhost:5000**

## 🎨 Using the Web Interface

### Home Page Features

1. **Hero Section**: Introduction with key features
2. **Features Grid**: 8 feature cards showing capabilities
3. **Plans Section**: FEDVIP and VADIP 2025 plan details
4. **About Section**: Technology stack information
5. **Chat Icon**: Floating button in bottom-right corner

### Chat Modal

1. **Click Chat Icon**: Opens modal chat window
2. **Type Message**: Enter your question in the text area
3. **Send Message**: Click send button or press Enter
4. **View Response**: AI assistant responds in real-time
5. **Reset Chat**: Click refresh icon to clear conversation
6. **Close Modal**: Click X button to close (stays in background)

### Sample Questions to Try

```
- Show me my member information
- What are my dependents?
- List my recent claims
- What's my coverage for preventive care?
- How much does a root canal cost?
- Show my ID card
- What's covered under FEDVIP 2025?
- Tell me about VADIP benefits
- How much of my annual maximum have I used?
```

## 📁 File Structure

```
LangChain1/
├── app.py                      # Flask web application
├── templates/
│   └── index.html              # Home page template
├── static/
│   ├── css/
│   │   └── style.css           # Styles for UI and modal
│   └── js/
│       └── chat.js             # Chat functionality and API calls
├── main.py                     # Original CLI application
├── agent.py                    # LangChain chatbot
├── mcp_server.py              # MCP tools
├── rag_pipeline.py            # RAG implementation
├── config.py                  # Configuration
├── models.py                  # Data models
└── .env                       # Environment variables
```

## 🔌 API Endpoints

### POST /api/chat

Send a chat message and get AI response.

**Request:**

```json
{
  "message": "What is my coverage?"
}
```

**Response:**

```json
{
  "response": "Your coverage includes...",
  "session_id": "uuid-here"
}
```

### POST /api/reset

Reset the conversation history.

**Response:**

```json
{
  "message": "Conversation reset successfully"
}
```

### GET /api/member-info

Get current member information.

**Response:**

```json
{
  "id": "MEM001",
  "name": "John Smith",
  "email": "john.smith@example.com",
  "phone": "(555) 123-4567",
  "date_of_birth": "1980-05-15"
}
```

### GET /health

Health check endpoint.

**Response:**

```json
{
  "status": "healthy",
  "chatbot_initialized": true,
  "data_store_initialized": true,
  "rag_pipeline_initialized": true
}
```

## 🎨 Customization

### Modify Home Page Content

Edit `templates/index.html`:

- Change hero text, features, plans
- Add new sections
- Update footer information

### Customize Styles

Edit `static/css/style.css`:

- Change colors (see `:root` variables)
- Modify layout, spacing, fonts
- Adjust modal size and position
- Update animations

### Extend Chat Functionality

Edit `static/js/chat.js`:

- Add new message formatting
- Implement additional features
- Modify chat behavior
- Add typing indicators

### Add New API Endpoints

Edit `app.py`:

- Create new routes
- Add data endpoints
- Implement additional features

## 🔒 Security Considerations

### Production Deployment

1. **Secret Key**: Set a strong `FLASK_SECRET_KEY` in `.env`
2. **HTTPS**: Use HTTPS in production (SSL/TLS certificates)
3. **CORS**: Configure `flask-cors` for specific origins
4. **Rate Limiting**: Add rate limiting for API endpoints
5. **Authentication**: Implement user authentication if needed
6. **Environment**: Set `FLASK_DEBUG=False` in production

### Example Production Configuration

```python
# app.py - Production settings
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/chat', methods=['POST'])
@limiter.limit("30 per minute")
def chat():
    # ... existing code
```

## 🚀 Deployment Options

### 1. Local Development

```powershell
python app.py
# Access at http://localhost:5000
```

### 2. Docker Container

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

```powershell
docker build -t dental-chatbot .
docker run -p 5000:5000 --env-file .env dental-chatbot
```

### 3. Cloud Deployment (Azure)

```powershell
# Azure App Service
az webapp up --name dental-chatbot --runtime "PYTHON:3.12"

# Configure environment variables
az webapp config appsettings set --name dental-chatbot --settings @.env
```

### 4. Other Hosting Options

- **Heroku**: `heroku create && git push heroku main`
- **Google Cloud Run**: Deploy container with Cloud Run
- **AWS Elastic Beanstalk**: Deploy Flask application
- **DigitalOcean App Platform**: Deploy from GitHub

## 🧪 Testing the Web App

### Manual Testing

1. **Home Page**: Verify all sections load correctly
2. **Chat Icon**: Click to open modal
3. **Send Message**: Test chat functionality
4. **Reset**: Clear conversation and verify
5. **Close/Open**: Test modal toggle
6. **Mobile View**: Test responsive design
7. **API Endpoints**: Test with curl or Postman

### Automated Testing

```python
# test_web_app.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Dental Insurance Assistant' in response.data

def test_chat_endpoint(client):
    response = client.post('/api/chat',
                          json={'message': 'Hello'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'response' in data
```

## 🐛 Troubleshooting

### Issue: Flask not found

```powershell
pip install Flask flask-cors
```

### Issue: Port already in use

```powershell
# Change port in .env
FLASK_PORT=8080
```

Or kill the process:

```powershell
# Find process using port 5000
netstat -ano | findstr :5000
# Kill process (replace PID)
taskkill /PID <PID> /F
```

### Issue: LLM not responding

1. Check LM Studio is running (http://localhost:1234)
2. Verify `.env` configuration
3. Check `config.py` settings
4. View Flask console for errors

### Issue: Static files not loading

- Clear browser cache
- Check file paths in `templates/index.html`
- Verify `static/` folder structure
- Restart Flask server

### Issue: Session not persisting

- Set `FLASK_SECRET_KEY` in `.env`
- Check browser cookies are enabled
- Verify Flask session configuration

## 📊 Monitoring and Logs

### View Logs

Flask prints logs to console:

- Request URLs and methods
- Response status codes
- Error messages and tracebacks
- Chatbot initialization status

### Add Custom Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    logger.info(f"Chat request: {request.get_json()}")
    # ... existing code
```

## 🎯 Next Steps

1. **Deploy to Production**: Choose hosting platform and deploy
2. **Add Authentication**: Implement user login/signup
3. **Database Integration**: Store chat history in database
4. **Analytics**: Track usage and popular queries
5. **Advanced Features**: Add file uploads, voice input, etc.
6. **Mobile App**: Create React Native or Flutter app

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-CORS](https://flask-cors.readthedocs.io/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)
- [LangChain Documentation](https://python.langchain.com/)

## 💡 Tips

- Keep Flask console open to see real-time logs
- Use browser DevTools to debug JavaScript
- Test API endpoints with Postman or curl
- Enable FLASK_DEBUG=True for development
- Use virtual environment for dependency isolation

---

**Ready to chat!** 🚀 Open http://localhost:5000 and click the chat icon to start!
