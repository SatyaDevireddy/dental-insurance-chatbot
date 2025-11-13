"""
Test script to download and preview the MetLife FEDVIP 2025 PDF
"""
from pdf_loader import load_metlife_fedvip_2025

if __name__ == "__main__":
    print("="*70)
    print("MetLife FEDVIP 2025 PDF Loader Test")
    print("="*70)
    print()
    
    try:
        # Load the PDF
        doc = load_metlife_fedvip_2025()
        
        print("\n" + "="*70)
        print("Document Information")
        print("="*70)
        print(f"Document ID: {doc.document_id}")
        print(f"Plan ID: {doc.plan_id}")
        print(f"Title: {doc.title}")
        print(f"Type: {doc.document_type}")
        print(f"Last Updated: {doc.last_updated}")
        print(f"Content Length: {len(doc.content):,} characters")
        
        print("\n" + "="*70)
        print("First 1000 Characters of Extracted Content")
        print("="*70)
        print(doc.content[:1000])
        
        print("\n" + "="*70)
        print("✅ PDF successfully loaded and processed!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
