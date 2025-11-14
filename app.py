"""
Flask Web Application for Dental Insurance Chatbot
Provides a web interface with modal chatbot functionality
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
from dotenv import load_dotenv
import uuid

# Import chatbot components
from config import load_config, validate_config
from models import Member, Dependent
from mcp_server import InsuranceDataStore, MCPInsuranceTools
from rag_pipeline import RAGPipeline
from agent import DentalInsuranceChatbot
from sample_data import initialize_sample_data
from pdf_loader import load_metlife_fedvip_2025, load_metlife_vadip

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dental-insurance-chatbot-secret-key-' + str(uuid.uuid4()))
CORS(app)

# Global instances
chatbot = None
data_store = None
mcp_tools = None
rag_pipeline = None


def initialize_system():
    """Initialize the chatbot system"""
    global chatbot, data_store, mcp_tools, rag_pipeline
    
    print("🚀 Initializing Dental Insurance Chatbot Web Application...")
    
    # Load and validate configuration
    config = load_config()
    validate_config(config)
    
    # Initialize data store and sample data
    data_store = InsuranceDataStore()
    initialize_sample_data(data_store)
    print("✅ Sample data loaded")
    
    # Initialize MCP tools
    mcp_tools = MCPInsuranceTools(data_store)
    print("✅ MCP tools initialized")
    
    # Initialize RAG pipeline
    rag_pipeline = RAGPipeline()
    
    # Load FEDVIP 2025 plan document
    try:
        fedvip_doc = load_metlife_fedvip_2025()
        rag_pipeline.add_documents([fedvip_doc])
        print("✅ MetLife FEDVIP 2025 plan loaded")
    except Exception as e:
        print(f"⚠️ Warning: Could not load FEDVIP 2025 plan: {e}")
    
    # Load VADIP plan document
    try:
        vadip_doc = load_metlife_vadip()
        rag_pipeline.add_documents([vadip_doc])
        print("✅ MetLife VADIP 2025 plan loaded")
    except Exception as e:
        print(f"⚠️ Warning: Could not load VADIP 2025 plan: {e}")
    
    # Initialize chatbot
    chatbot = DentalInsuranceChatbot(
        mcp_tools=mcp_tools,
        rag_pipeline=rag_pipeline,
        llm_provider=config.provider,
        member_id=os.getenv('CURRENT_MEMBER_ID', 'MEM001')
    )
    print("✅ Chatbot initialized")
    print("🌐 Web application ready!")


@app.route('/')
def home():
    """Render the home page"""
    # Always render the page - member info is optional
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages from the web interface"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get or create session ID for conversation history
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        # Get chatbot response
        if chatbot:
            response = chatbot.chat(message)
            return jsonify({
                'response': response,
                'session_id': session['session_id']
            })
        else:
            return jsonify({'error': 'Chatbot not initialized'}), 500
            
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def reset_chat():
    """Reset the chat conversation"""
    try:
        if chatbot:
            chatbot.reset_conversation()
        
        # Clear session
        session.pop('session_id', None)
        
        return jsonify({'message': 'Conversation reset successfully'})
    except Exception as e:
        print(f"Error resetting chat: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/member-info')
def get_member_info():
    """Get current member information"""
    try:
        if mcp_tools:
            member_id = os.getenv('CURRENT_MEMBER_ID', 'MEM001')
            member_info = mcp_tools.get_member_info(member_id)
            return jsonify(member_info)
        
        return jsonify({'error': 'MCP tools not initialized'}), 500
    except Exception as e:
        print(f"Error getting member info: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'chatbot_initialized': chatbot is not None,
        'data_store_initialized': data_store is not None,
        'mcp_tools_initialized': mcp_tools is not None,
        'rag_pipeline_initialized': rag_pipeline is not None
    })


@app.route('/test')
def test():
    """Test route to verify Flask is working"""
    return "Flask is working! ✅"


if __name__ == '__main__':
    # Initialize the system before starting the server
    initialize_system()
    
    # Get port from environment or use default
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"\n🌐 Starting web server on http://localhost:{port}")
    print("📱 Open your browser and navigate to the URL above")
    print("💬 Click the chat icon to start chatting!\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
