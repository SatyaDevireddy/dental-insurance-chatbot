"""
Main application for Dental Insurance Chatbot

This is the entry point for the chatbot application.
"""
import sys
import os
from datetime import date, datetime
from config import load_config, validate_config, print_config
from mcp_server import InsuranceDataStore, MCPInsuranceTools
from rag_pipeline import RAGPipeline, create_sample_plan_documents
from agent import DentalInsuranceChatbot
from sample_data import initialize_sample_data
from pdf_loader import load_metlife_fedvip_2025, load_metlife_vadip


def initialize_system():
    """
    Initialize the chatbot system with data and configuration.
    
    Returns:
        Tuple of (config, chatbot) or (None, None) if initialization fails
    """
    print("Initializing Dental Insurance Chatbot...")
    print()
    
    # Load configuration
    config = load_config()
    
    # Validate configuration
    is_valid, error_msg = validate_config(config)
    if not is_valid:
        print(f"❌ Configuration Error: {error_msg}")
        print("\nPlease check your .env file and ensure all required variables are set.")
        return None, None
    
    # Print configuration
    print_config(config)
    
    # Initialize data store
    print("📦 Loading insurance data...")
    data_store = InsuranceDataStore()
    initialize_sample_data(data_store)
    print("✅ Insurance data loaded")
    
    # Initialize MCP tools
    print("🔧 Initializing MCP tools...")
    mcp_tools = MCPInsuranceTools(data_store)
    print("✅ MCP tools initialized")
    
    # Initialize RAG pipeline
    print("🧠 Initializing RAG pipeline...")
    rag_pipeline = RAGPipeline(
        persist_directory=config.chroma_persist_directory,
        embedding_model=config.embedding_model
    )
    
    # Add sample documents if vector store is empty
    print("📚 Loading plan documents...")
    plan_documents = create_sample_plan_documents()
    rag_pipeline.add_documents(plan_documents)
    
    # Load MetLife FEDVIP 2025 PDF document
    print("📥 Loading MetLife FEDVIP 2025 PDF...")
    try:
        metlife_fedvip_doc = load_metlife_fedvip_2025()
        rag_pipeline.add_documents([metlife_fedvip_doc])
        print("✅ MetLife FEDVIP 2025 PDF loaded and indexed")
    except Exception as e:
        print(f"⚠️  Warning: Could not load MetLife FEDVIP PDF: {str(e)}")
        print("   Continuing without FEDVIP document...")
    
    # Load MetLife VADIP PDF document
    print("📥 Loading MetLife VADIP PDF...")
    try:
        metlife_vadip_doc = load_metlife_vadip()
        rag_pipeline.add_documents([metlife_vadip_doc])
        print("✅ MetLife VADIP PDF loaded and indexed")
    except Exception as e:
        print(f"⚠️  Warning: Could not load MetLife VADIP PDF: {str(e)}")
        print("   Continuing without VADIP document...")
    
    print("✅ Plan documents loaded")
    
    # Initialize chatbot
    print("🤖 Initializing chatbot agent...")
    chatbot = DentalInsuranceChatbot(
        mcp_tools=mcp_tools,
        rag_pipeline=rag_pipeline,
        llm_provider=config.provider,
        member_id=config.current_member_id
    )
    print("✅ Chatbot agent initialized")
    print()
    
    return config, chatbot


def print_welcome_message(config):
    """Print welcome message with instructions."""
    print("\n" + "="*60)
    print("🦷 DENTAL INSURANCE CHATBOT")
    print("="*60)
    print("\nWelcome! I'm your dental insurance assistant.")
    print(f"Current Member ID: {config.current_member_id or 'Not set'}")
    print()
    print("I can help you with:")
    print("  • Viewing your claims and claim status")
    print("  • Understanding your coverage and benefits")
    print("  • Looking up dental procedures and costs")
    print("  • Checking your ID card information")
    print("  • Answering questions about your plan")
    print("  • Finding information about dependents")
    print()
    print("Commands:")
    print("  • Type your question and press Enter")
    print("  • Type 'quit' or 'exit' to end the conversation")
    print("  • Type 'reset' to start a new conversation")
    print("  • Type 'help' for more information")
    print("="*60 + "\n")


def print_help():
    """Print help information."""
    print("\n" + "="*60)
    print("HELP - Example Questions")
    print("="*60)
    print("\nHere are some example questions you can ask:")
    print()
    print("Claims:")
    print("  • What are my recent claims?")
    print("  • Show me claims from last month")
    print("  • What's the status of claim CLM001?")
    print()
    print("Coverage:")
    print("  • What does my plan cover?")
    print("  • How much does a crown cost?")
    print("  • What's my annual maximum?")
    print("  • Do I have a deductible?")
    print()
    print("Procedures:")
    print("  • What is a root canal?")
    print("  • Search for cleaning procedures")
    print("  • Is a crown covered?")
    print()
    print("General:")
    print("  • Show me my ID card")
    print("  • Who are my dependents?")
    print("  • How much of my benefits have I used?")
    print("  • What's the waiting period for major services?")
    print("="*60 + "\n")


def run_chatbot_loop(chatbot, config):
    """
    Run the main chatbot conversation loop.
    
    Args:
        chatbot: DentalInsuranceChatbot instance
        config: LLMConfig instance
    """
    print_welcome_message(config)
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Handle empty input
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Thank you for using the Dental Insurance Chatbot. Have a great day!")
                break
            
            elif user_input.lower() == 'reset':
                chatbot.reset_conversation()
                print("\n🔄 Conversation reset. How can I help you?\n")
                continue
            
            elif user_input.lower() == 'help':
                print_help()
                continue
            
            # Process the message
            print("\n🤖 Assistant: ", end="", flush=True)
            response = chatbot.chat(user_input)
            print(response)
            print()
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            print("Please try again or type 'quit' to exit.\n")


def main():
    """Main entry point for the application."""
    try:
        # Initialize system
        config, chatbot = initialize_system()
        
        if config is None or chatbot is None:
            print("\n❌ Failed to initialize the chatbot. Please check your configuration.")
            sys.exit(1)
        
        # Run chatbot loop
        run_chatbot_loop(chatbot, config)
    
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
