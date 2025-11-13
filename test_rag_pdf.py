"""
Test script to verify PDF is queryable in RAG pipeline
"""
import sys
from config import load_config
from rag_pipeline import RAGPipeline, create_sample_plan_documents
from pdf_loader import load_metlife_fedvip_2025

def test_pdf_rag():
    print("="*70)
    print("Testing MetLife FEDVIP PDF in RAG Pipeline")
    print("="*70)
    print()
    
    # Load config
    config = load_config()
    
    # Initialize RAG pipeline
    print("🧠 Initializing RAG pipeline...")
    rag = RAGPipeline(
        persist_directory=config.chroma_persist_directory,
        embedding_model=config.embedding_model
    )
    
    # Load sample documents
    print("📚 Loading sample documents...")
    sample_docs = create_sample_plan_documents()
    rag.add_documents(sample_docs)
    
    # Load MetLife PDF
    print("📥 Loading MetLife FEDVIP 2025 PDF...")
    try:
        metlife_doc = load_metlife_fedvip_2025()
        rag.add_documents([metlife_doc])
        print("✅ MetLife PDF loaded\n")
    except Exception as e:
        print(f"❌ Error loading PDF: {e}\n")
        return
    
    # Test queries
    test_queries = [
        "What are the rates for MetLife FEDVIP?",
        "What services are covered under MetLife federal dental?",
        "When is open enrollment for FEDVIP?",
        "What are the savings with MetLife federal plan?",
        "What is the coverage percentage for routine services?"
    ]
    
    print("="*70)
    print("Testing RAG Retrieval")
    print("="*70)
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        print("-" * 70)
        
        # Retrieve relevant documents
        docs = rag.retrieve_relevant_docs(query, k=2)
        
        if docs:
            for i, doc in enumerate(docs, 1):
                print(f"\n  Result {i}:")
                print(f"  Title: {doc.metadata.get('title', 'Unknown')}")
                print(f"  Content preview: {doc.page_content[:200]}...")
        else:
            print("  ⚠️  No relevant documents found")
    
    print("\n" + "="*70)
    print("✅ RAG Pipeline Test Complete!")
    print("="*70)

if __name__ == "__main__":
    test_pdf_rag()
