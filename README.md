# Dental Insurance Member Chatbot

A comprehensive dental insurance chatbot built with LangChain that uses **RAG (Retrieval Augmented Generation)** and **MCP (Model Context Protocol)** concepts to help members query their claims, coverages, procedures, ID cards, and other plan information.

## 🎯 Features

- **Member Information**: Query personal information and dependents
- **Claims Management**: View claim history, status, and details
- **Coverage Details**: Understand benefit coverage, deductibles, and annual maximums
- **Procedure Information**: Search for dental procedures and their costs
- **ID Card Access**: Retrieve member ID card information
- **Benefit Usage Tracking**: Check how much of annual benefits have been used
- **RAG-Powered Answers**: Search plan documents for policy information, FAQs, and more
- **PDF Document Integration**: Load and query real insurance plan PDFs (e.g., MetLife FEDVIP 2025)
- **MCP Tools**: Structured data access through Model Context Protocol
- **Multi-LLM Support**: Works with local LLMs (via OpenAI API) and Azure OpenAI

## 🏗️ Architecture

### Components

1. **Data Models** (`models.py`)

   - Pydantic models for members, claims, coverage, procedures, etc.
   - Type-safe data structures

2. **MCP Server** (`mcp_server.py`)

   - Model Context Protocol implementation
   - Exposes 8 insurance data tools to the agent
   - In-memory data store (simulated database)

3. **RAG Pipeline** (`rag_pipeline.py`)

   - ChromaDB vector store for plan documents
   - Sentence transformers for embeddings
   - Document retrieval and search

4. **LangChain Agent** (`agent.py`)

   - OpenAI tools agent with function calling
   - Integrates MCP tools and RAG retrieval
   - Conversational memory

5. **Configuration** (`config.py`)

   - Environment-based configuration
   - Support for local and Azure OpenAI
   - Validation and settings management

6. **Sample Data** (`sample_data.py`)

   - Pre-populated test data
   - Realistic insurance scenarios

7. **PDF Loader** (`pdf_loader.py`)
   - Download and process PDF documents
   - Extract text from insurance plan PDFs
   - Includes MetLife FEDVIP 2025 plan integration
   - Realistic insurance scenarios

## 📋 Prerequisites

- Python 3.9 or higher
- For local LLM: A local LLM server with OpenAI-compatible API (e.g., LM Studio, Ollama, llama.cpp)
- For Azure: Azure OpenAI resource with deployment

## 🚀 Installation

### 1. Clone or Download

Download the project files to your local machine.

### 2. Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment

Copy the example environment file and configure it:

```powershell
cp .env.example .env
```

Edit `.env` with your settings:

#### For Local LLM (Default):

```env
LLM_PROVIDER=local
LOCAL_API_BASE=http://localhost:1234/v1
LOCAL_API_KEY=not-needed
LOCAL_MODEL_NAME=local-model
CURRENT_MEMBER_ID=MEM001
```

#### For Azure OpenAI:

```env
LLM_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview
CURRENT_MEMBER_ID=MEM001
```

## 🎮 Usage

### Running the Chatbot

```powershell
python main.py
```

### Example Interactions

```
You: What are my recent claims?

🤖 Assistant: Let me check your recent claims...
[Shows claims with dates, procedures, amounts, and status]

You: How much of my annual maximum have I used?

🤖 Assistant: Let me look up your benefit usage...
You've used $915 of your $2,000 annual maximum, leaving $1,085 remaining.

You: What does my plan cover for cleanings?

🤖 Assistant: [Searches plan documents]
Your plan covers preventive care at 100% with no deductible...

You: Show me my ID card information

🤖 Assistant: Here's your ID card information:
Member: John Smith
Member ID: MEM001-001
Group Number: GRP12345
...
```

### Commands

- Type your question and press Enter
- `help` - Show example questions
- `reset` - Start a new conversation
- `quit` or `exit` - Exit the chatbot

## 🔧 MCP Tools Available

The chatbot has access to these tools:

1. **get_member_info** - Retrieve member information
2. **get_dependents** - List all dependents
3. **get_claims** - Query claims with filters
4. **get_coverage_details** - View coverage breakdown
5. **get_procedure_info** - Look up procedure details
6. **get_id_card** - Get ID card information
7. **get_benefit_usage** - Check benefit usage
8. **search_procedures** - Search for procedures
9. **search_plan_documents** - RAG-based document search

## 📊 Sample Data

The system comes pre-loaded with sample data:

- **Member**: John Smith (MEM001)
- **Dependents**: Spouse (Jane), Children (Emily, Michael)
- **Claims**: 6 sample claims with various statuses
- **Procedures**: 20 common dental procedures
- **Plan Documents**: Benefits summary, policies, FAQs, provider directory

## 🔄 RAG Implementation

The RAG pipeline uses:

- **Vector Store**: ChromaDB for persistent storage
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Documents**: Insurance policies, FAQs, benefits summaries
- **Retrieval**: Semantic search with metadata filtering

## 🌐 Azure Migration

To migrate from local LLM to Azure OpenAI:

1. Update `.env` file with Azure credentials
2. Change `LLM_PROVIDER=azure`
3. Restart the application

The code automatically handles the provider switch - no code changes needed!

## 📁 Project Structure

```
LangChain1/
├── main.py                 # Entry point
├── agent.py                # LangChain agent implementation
├── config.py               # Configuration management
├── models.py               # Data models (Pydantic)
├── mcp_server.py          # MCP tools and data store
├── rag_pipeline.py        # RAG implementation
├── sample_data.py         # Sample data initialization
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── .env                   # Your configuration (not in git)
├── .gitignore            # Git ignore file
└── data/
    └── chroma_db/        # Vector store (created on first run)
```

## 🛠️ Customization

### Adding New Members

Edit `sample_data.py` to add more members, dependents, and claims.

### Adding Plan Documents

In `rag_pipeline.py`, add more `PlanDocument` objects to the `create_sample_plan_documents()` function.

### Adding New MCP Tools

1. Add method to `MCPInsuranceTools` class in `mcp_server.py`
2. Add tool definition to `get_tool_definitions()`
3. Add LangChain tool wrapper in `agent.py`

### Changing Embedding Model

Update `EMBEDDING_MODEL` in `.env` to use a different sentence-transformers model.

## 🔍 Troubleshooting

### Import Errors

The lint errors shown during creation are expected - they'll resolve once dependencies are installed:

```powershell
pip install -r requirements.txt
```

### Local LLM Not Connecting

- Ensure your local LLM server is running
- Check the `LOCAL_API_BASE` URL matches your server
- Test with: `curl http://localhost:1234/v1/models`

### Azure OpenAI Errors

- Verify endpoint URL format
- Check API key is valid
- Ensure deployment name exists
- Verify API version is supported

### Vector Store Issues

- Delete `data/chroma_db/` folder to reset
- Check disk space availability
- Ensure write permissions

## 🚀 Production Considerations

For production deployment:

1. **Database**: Replace `InsuranceDataStore` with real database connections
2. **Authentication**: Add proper member authentication
3. **Security**: Use Azure Key Vault or AWS Secrets Manager for credentials
4. **Logging**: Add comprehensive logging and monitoring
5. **Rate Limiting**: Implement API rate limiting
6. **Caching**: Cache frequently accessed data
7. **Scalability**: Deploy with load balancing
8. **HIPAA Compliance**: Ensure PHI data protection

## 📚 Technologies Used

- **LangChain**: Agent framework and orchestration
- **ChromaDB**: Vector database for RAG
- **Sentence Transformers**: Text embeddings
- **Pydantic**: Data validation and models
- **OpenAI API**: LLM interface (local or Azure)
- **Python-dotenv**: Environment configuration

## 🤝 Contributing

To extend the chatbot:

1. Add new data models in `models.py`
2. Create corresponding MCP tools in `mcp_server.py`
3. Integrate tools into agent in `agent.py`
4. Update sample data in `sample_data.py`
5. Add documentation in this README

## 📝 License

This project is provided as-is for educational and development purposes.

## 🆘 Support

For issues or questions:

1. Check the troubleshooting section
2. Review example questions with `help` command
3. Verify configuration in `.env` file
4. Check Python version compatibility

## 🎓 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [RAG Overview](https://python.langchain.com/docs/use_cases/question_answering/)
- [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/)

---

**Built with ❤️ using LangChain, RAG, and MCP**
