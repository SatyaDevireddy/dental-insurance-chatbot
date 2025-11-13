"""
RAG (Retrieval Augmented Generation) Pipeline for Plan Documents

This module handles document loading, embedding, and retrieval using ChromaDB.
"""
import os
from typing import List, Dict, Any
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from models import PlanDocument


class RAGPipeline:
    """
    RAG pipeline for retrieving relevant plan document information.
    """
    
    def __init__(self, persist_directory: str = "./data/chroma_db", embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize the RAG pipeline.
        
        Args:
            persist_directory: Directory to persist the vector store
            embedding_model: Name of the sentence-transformers model to use
        """
        self.persist_directory = persist_directory
        self.embedding_model_name = embedding_model
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        # Initialize or load vector store
        self.vector_store = None
        self._init_vector_store()
    
    def _init_vector_store(self):
        """Initialize or load existing vector store."""
        if os.path.exists(self.persist_directory):
            # Load existing vector store
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        else:
            # Create new vector store (will be populated later)
            self.vector_store = None
    
    def add_documents(self, plan_documents: List[PlanDocument]):
        """
        Add plan documents to the vector store.
        
        Args:
            plan_documents: List of PlanDocument objects to add
        """
        documents = []
        
        for plan_doc in plan_documents:
            # Create LangChain Document objects with metadata
            doc = Document(
                page_content=plan_doc.content,
                metadata={
                    "document_id": plan_doc.document_id,
                    "plan_id": plan_doc.plan_id,
                    "document_type": plan_doc.document_type,
                    "title": plan_doc.title,
                    "last_updated": plan_doc.last_updated.isoformat()
                }
            )
            documents.append(doc)
        
        # Split documents into chunks
        split_docs = self.text_splitter.split_documents(documents)
        
        # Create or update vector store
        if self.vector_store is None:
            self.vector_store = Chroma.from_documents(
                documents=split_docs,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
        else:
            self.vector_store.add_documents(split_docs)
        
        # Persist the vector store
        self.vector_store.persist()
    
    def retrieve_relevant_docs(
        self, 
        query: str, 
        k: int = 4,
        filter_dict: Dict[str, Any] = None
    ) -> List[Document]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: The search query
            k: Number of documents to retrieve
            filter_dict: Optional metadata filter
            
        Returns:
            List of relevant Document objects
        """
        if self.vector_store is None:
            return []
        
        if filter_dict:
            docs = self.vector_store.similarity_search(
                query,
                k=k,
                filter=filter_dict
            )
        else:
            docs = self.vector_store.similarity_search(query, k=k)
        
        return docs
    
    def retrieve_with_scores(
        self, 
        query: str, 
        k: int = 4,
        filter_dict: Dict[str, Any] = None
    ) -> List[tuple]:
        """
        Retrieve relevant documents with similarity scores.
        
        Args:
            query: The search query
            k: Number of documents to retrieve
            filter_dict: Optional metadata filter
            
        Returns:
            List of tuples (Document, score)
        """
        if self.vector_store is None:
            return []
        
        if filter_dict:
            docs_with_scores = self.vector_store.similarity_search_with_score(
                query,
                k=k,
                filter=filter_dict
            )
        else:
            docs_with_scores = self.vector_store.similarity_search_with_score(query, k=k)
        
        return docs_with_scores
    
    def get_retriever(self, k: int = 4):
        """
        Get a LangChain retriever interface.
        
        Args:
            k: Number of documents to retrieve
            
        Returns:
            Retriever object
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Add documents first.")
        
        return self.vector_store.as_retriever(search_kwargs={"k": k})


def create_sample_plan_documents() -> List[PlanDocument]:
    """
    Create sample plan documents for testing.
    
    Returns:
        List of sample PlanDocument objects
    """
    from datetime import date
    
    documents = [
        PlanDocument(
            document_id="DOC001",
            plan_id="PLAN001",
            document_type="benefits_summary",
            title="Dental Benefits Summary",
            content="""
            Your dental insurance plan provides comprehensive coverage for preventive, basic, and major dental services.
            
            PREVENTIVE CARE (100% Coverage):
            - Routine cleanings and exams (twice per year)
            - X-rays (bitewings once per year, full mouth every 3 years)
            - Fluoride treatments (for children under 18)
            - Sealants (for children under 18)
            
            BASIC SERVICES (80% Coverage after deductible):
            - Fillings (amalgam and composite)
            - Simple extractions
            - Emergency care
            - Root canals
            
            MAJOR SERVICES (50% Coverage after deductible):
            - Crowns and bridges
            - Dentures and partials
            - Implants
            - Complex oral surgery
            
            ORTHODONTIC SERVICES (50% Coverage):
            - Braces for children and adults
            - Lifetime maximum of $2,000
            
            ANNUAL MAXIMUM: $2,000 per person (does not include preventive care)
            ANNUAL DEDUCTIBLE: $50 per person, $150 per family
            """,
            last_updated=date(2024, 1, 1)
        ),
        PlanDocument(
            document_id="DOC002",
            plan_id="PLAN001",
            document_type="policy",
            title="Waiting Periods and Limitations",
            content="""
            WAITING PERIODS:
            - No waiting period for preventive and basic services
            - 6 months waiting period for major services
            - 12 months waiting period for orthodontic services
            
            FREQUENCY LIMITATIONS:
            - Cleanings: Maximum 2 per calendar year
            - Exams: Maximum 2 per calendar year
            - Fluoride: Once per calendar year (children only)
            - Bitewing X-rays: Once per calendar year
            - Full mouth X-rays: Once every 3 years
            - Crowns: Once every 5 years per tooth
            
            EXCLUSIONS:
            - Cosmetic procedures (teeth whitening, veneers for appearance only)
            - Services primarily for cosmetic purposes
            - Lost or stolen appliances
            - Services covered by workers' compensation
            - Services not dentally necessary
            
            PRE-AUTHORIZATION:
            Required for any treatment over $300. Submit treatment plan to insurance
            before proceeding with major services.
            """,
            last_updated=date(2024, 1, 1)
        ),
        PlanDocument(
            document_id="DOC003",
            plan_id="PLAN001",
            document_type="faq",
            title="Frequently Asked Questions",
            content="""
            Q: How do I file a claim?
            A: Most dentists will file claims directly with your insurance. If you need to file
            yourself, complete a claim form and submit with itemized receipts to the claims address
            on your ID card within 90 days of service.
            
            Q: Can I go to any dentist?
            A: Yes, this is a PPO plan. You can see any licensed dentist, but you'll save more with
            in-network providers who have agreed to discounted fees.
            
            Q: What if I need a crown?
            A: Crowns are considered major services and are covered at 50% after your deductible.
            Pre-authorization is required. The waiting period is 6 months from your effective date.
            
            Q: Are implants covered?
            A: Yes, dental implants are covered at 50% as a major service, subject to your annual
            maximum and after the 6-month waiting period.
            
            Q: What about emergency dental care?
            A: Emergency care is covered as a basic service at 80% after deductible. No waiting
            period applies for emergency services.
            
            Q: How do I add a dependent?
            A: Contact member services within 31 days of a qualifying event (birth, adoption, marriage).
            Coverage will be effective from the date of the event.
            
            Q: What is the appeals process?
            A: If a claim is denied, you have 180 days to file an appeal. Submit a written request
            with supporting documentation to the appeals department.
            """,
            last_updated=date(2024, 1, 1)
        ),
        PlanDocument(
            document_id="DOC004",
            plan_id="PLAN001",
            document_type="provider_directory",
            title="Finding a Dentist",
            content="""
            FINDING IN-NETWORK PROVIDERS:
            Use our online provider directory at www.dentalinsurance.com/find-dentist
            or call customer service at 1-800-DENTAL-1.
            
            IN-NETWORK BENEFITS:
            - Lower out-of-pocket costs
            - No claim forms to file
            - Pre-negotiated fees
            - Direct payment to provider
            
            OUT-OF-NETWORK BENEFITS:
            - You may need to pay upfront and file claims
            - Reimbursed based on usual and customary rates
            - May have higher out-of-pocket costs
            
            CHANGING DENTISTS:
            You can change dentists at any time. No referrals needed. Simply call to make an
            appointment and provide your member ID.
            
            SPECIALTY CARE:
            Coverage includes specialists such as:
            - Endodontists (root canals)
            - Periodontists (gum disease)
            - Oral surgeons
            - Orthodontists (braces)
            - Pediatric dentists
            """,
            last_updated=date(2024, 1, 1)
        )
    ]
    
    return documents
