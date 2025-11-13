"""
Configuration module for LLM providers (Local and Azure OpenAI)
"""
import os
from typing import Optional
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class LLMConfig:
    """Configuration for LLM providers."""
    provider: str  # "local" or "azure"
    
    # Local LLM settings
    local_api_base: Optional[str] = None
    local_api_key: Optional[str] = None
    local_model_name: Optional[str] = None
    
    # Azure OpenAI settings
    azure_endpoint: Optional[str] = None
    azure_api_key: Optional[str] = None
    azure_deployment_name: Optional[str] = None
    azure_api_version: Optional[str] = None
    
    # Embedding settings
    embedding_model: str = "all-MiniLM-L6-v2"
    
    # Vector store settings
    chroma_persist_directory: str = "./data/chroma_db"
    
    # Member context
    current_member_id: Optional[str] = None


def load_config() -> LLMConfig:
    """
    Load configuration from environment variables.
    
    Returns:
        LLMConfig object with loaded settings
    """
    # Load .env file if it exists
    load_dotenv()
    
    provider = os.getenv("LLM_PROVIDER", "local").lower()
    
    config = LLMConfig(
        provider=provider,
        # Local settings
        local_api_base=os.getenv("LOCAL_API_BASE", "http://localhost:1234/v1"),
        local_api_key=os.getenv("LOCAL_API_KEY", "not-needed"),
        local_model_name=os.getenv("LOCAL_MODEL_NAME", "local-model"),
        # Azure settings
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        azure_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        # Other settings
        embedding_model=os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"),
        chroma_persist_directory=os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma_db"),
        current_member_id=os.getenv("CURRENT_MEMBER_ID")
    )
    
    return config


def validate_config(config: LLMConfig) -> tuple[bool, str]:
    """
    Validate the configuration.
    
    Args:
        config: LLMConfig object to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if config.provider == "azure":
        if not config.azure_endpoint:
            return False, "AZURE_OPENAI_ENDPOINT is required for Azure provider"
        if not config.azure_api_key:
            return False, "AZURE_OPENAI_API_KEY is required for Azure provider"
        if not config.azure_deployment_name:
            return False, "AZURE_OPENAI_DEPLOYMENT_NAME is required for Azure provider"
    
    elif config.provider == "local":
        if not config.local_api_base:
            return False, "LOCAL_API_BASE is required for local provider"
    
    else:
        return False, f"Unknown provider: {config.provider}. Must be 'local' or 'azure'"
    
    return True, ""


def print_config(config: LLMConfig):
    """Print current configuration (hiding sensitive data)."""
    print("\n" + "="*60)
    print("DENTAL INSURANCE CHATBOT CONFIGURATION")
    print("="*60)
    print(f"LLM Provider: {config.provider.upper()}")
    print()
    
    if config.provider == "local":
        print("Local LLM Settings:")
        print(f"  API Base: {config.local_api_base}")
        print(f"  Model: {config.local_model_name}")
    elif config.provider == "azure":
        print("Azure OpenAI Settings:")
        print(f"  Endpoint: {config.azure_endpoint}")
        print(f"  Deployment: {config.azure_deployment_name}")
        print(f"  API Version: {config.azure_api_version}")
        print(f"  API Key: {'*' * 10 if config.azure_api_key else 'Not set'}")
    
    print()
    print("Vector Store Settings:")
    print(f"  Embedding Model: {config.embedding_model}")
    print(f"  Persist Directory: {config.chroma_persist_directory}")
    
    print()
    print("Member Context:")
    print(f"  Current Member ID: {config.current_member_id or 'Not set'}")
    print("="*60 + "\n")
