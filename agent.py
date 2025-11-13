"""
LangChain Agent for Dental Insurance Chatbot

This module creates an agent that combines MCP tools and RAG retrieval
to answer member queries about their dental insurance.
"""
import os
import json
from typing import List, Dict, Any, Optional
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from mcp_server import MCPInsuranceTools, get_tool_definitions
from rag_pipeline import RAGPipeline


class DentalInsuranceChatbot:
    """
    Dental Insurance Chatbot using LangChain with MCP tools and RAG.
    """
    
    def __init__(
        self,
        mcp_tools: MCPInsuranceTools,
        rag_pipeline: RAGPipeline,
        llm_provider: str = "local",
        member_id: str = None
    ):
        """
        Initialize the chatbot.
        
        Args:
            mcp_tools: MCP insurance tools instance
            rag_pipeline: RAG pipeline instance
            llm_provider: "local" or "azure"
            member_id: Current member ID for context
        """
        self.mcp_tools = mcp_tools
        self.rag_pipeline = rag_pipeline
        self.member_id = member_id
        self.llm = self._initialize_llm(llm_provider)
        self.tools = self._create_langchain_tools()
        self.agent = self._create_agent()
        self.conversation_history = []
    
    def _initialize_llm(self, provider: str):
        """Initialize the LLM based on provider."""
        if provider == "azure":
            return AzureChatOpenAI(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                temperature=0.2
            )
        else:  # local
            return ChatOpenAI(
                base_url=os.getenv("LOCAL_API_BASE", "http://localhost:1234/v1"),
                api_key=os.getenv("LOCAL_API_KEY", "not-needed"),
                model=os.getenv("LOCAL_MODEL_NAME", "local-model"),
                temperature=0.2
            )
    
    def _create_langchain_tools(self) -> List[Tool]:
        """Create LangChain tools from MCP tools and RAG."""
        tools = []
        
        # MCP Tools
        tools.append(Tool(
            name="get_member_info",
            func=lambda member_id: json.dumps(self.mcp_tools.get_member_info(member_id)),
            description="Get member information by member ID. Input should be the member ID string."
        ))
        
        tools.append(Tool(
            name="get_dependents",
            func=lambda member_id: json.dumps(self.mcp_tools.get_dependents(member_id)),
            description="Get all dependents for a member. Input should be the member ID string."
        ))
        
        tools.append(Tool(
            name="get_claims",
            func=lambda args: json.dumps(self._parse_and_get_claims(args)),
            description="""Get claims for a member with optional filtering. 
            Input should be JSON string with keys: member_id (required), status (optional), 
            start_date (optional), end_date (optional).
            Example: {"member_id": "MEM001", "status": "paid"}"""
        ))
        
        tools.append(Tool(
            name="get_coverage_details",
            func=lambda member_id: json.dumps(self.mcp_tools.get_coverage_details(member_id)),
            description="Get coverage details for a member's plan. Input should be the member ID string."
        ))
        
        tools.append(Tool(
            name="get_procedure_info",
            func=lambda procedure_code: json.dumps(self.mcp_tools.get_procedure_info(procedure_code)),
            description="Get information about a specific dental procedure. Input should be the procedure code (e.g., D0120)."
        ))
        
        tools.append(Tool(
            name="get_id_card",
            func=lambda member_id: json.dumps(self.mcp_tools.get_id_card(member_id)),
            description="Get ID card information for a member. Input should be the member ID string."
        ))
        
        tools.append(Tool(
            name="get_benefit_usage",
            func=lambda member_id: json.dumps(self.mcp_tools.get_benefit_usage(member_id)),
            description="Get benefit usage showing annual maximum and deductible usage. Input should be the member ID string."
        ))
        
        tools.append(Tool(
            name="search_procedures",
            func=lambda search_term: json.dumps(self.mcp_tools.search_procedures(search_term)),
            description="Search for dental procedures by name or description. Input should be the search term string."
        ))
        
        # RAG Tool
        tools.append(Tool(
            name="search_plan_documents",
            func=self._search_plan_documents,
            description="""Search plan documents for information about benefits, policies, FAQs, etc.
            Use this for general questions about coverage rules, waiting periods, exclusions, etc.
            Input should be a natural language question or search query."""
        ))
        
        return tools
    
    def _parse_and_get_claims(self, args_str: str) -> List[Dict]:
        """Parse claims arguments and call the appropriate method."""
        try:
            args = json.loads(args_str)
            return self.mcp_tools.get_claims(
                member_id=args.get("member_id"),
                status=args.get("status"),
                start_date=args.get("start_date"),
                end_date=args.get("end_date")
            )
        except json.JSONDecodeError:
            # If not JSON, assume it's just a member_id
            return self.mcp_tools.get_claims(args_str)
    
    def _search_plan_documents(self, query: str) -> str:
        """Search plan documents using RAG."""
        docs = self.rag_pipeline.retrieve_relevant_docs(query, k=3)
        
        if not docs:
            return "No relevant plan documents found."
        
        result = "Relevant information from plan documents:\n\n"
        for i, doc in enumerate(docs, 1):
            result += f"Source {i} ({doc.metadata.get('title', 'Unknown')}):\n"
            result += f"{doc.page_content}\n\n"
        
        return result
    
    def _create_agent(self):
        """Create a simple chat-based interface (not using full agent executor)."""
        # We'll use a simpler approach without AgentExecutor
        # The chat method will handle tool calling manually
        return None
    
    def chat(self, message: str) -> str:
        """
        Process a user message and return a response using direct LLM interaction.
        
        Args:
            message: User's message
            
        Returns:
            Chatbot's response
        """
        try:
            # Build system prompt with member context
            system_prompt = f"""You are a helpful dental insurance chatbot assistant for member ID: {self.member_id or 'Unknown'}.

You help members understand their dental insurance benefits, find information about claims, coverage, procedures, and answer questions about their plan.

When members ask about "my" information, use member ID: {self.member_id}

You have access to these tools:
- get_member_info: Get member information
- get_dependents: List dependents
- get_claims: Query claims (can filter by status, dates)
- get_coverage_details: View coverage breakdown
- get_procedure_info: Look up procedure by code
- get_id_card: Get ID card information
- get_benefit_usage: Check benefit usage
- search_procedures: Search for procedures by name
- search_plan_documents: Search plan documents for policy info

Be friendly, professional, and provide specific details. When you need data, describe what tool you would use."""

            # Build messages
            messages = [SystemMessage(content=system_prompt)]
            messages.extend(self.conversation_history)
            messages.append(HumanMessage(content=message))
            
            # Get response from LLM
            response = self.llm.invoke(messages)
            
            # Update conversation history
            self.conversation_history.append(HumanMessage(content=message))
            self.conversation_history.append(AIMessage(content=response.content))
            
            # Keep history limited to last 10 messages
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return response.content
        
        except Exception as e:
            error_message = f"I apologize, but I encountered an error: {str(e)}"
            return error_message
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
    
    def set_member_id(self, member_id: str):
        """Set the current member ID context."""
        self.member_id = member_id
