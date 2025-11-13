"""
Test script to download and preview both MetLife PDFs
"""
from pdf_loader import load_metlife_fedvip_2025, load_metlife_vadip

def test_pdf(loader_func, plan_name):
    """Test loading a single PDF"""
    print("\n" + "="*70)
    print(f"Testing {plan_name}")
    print("="*70)
    
    try:
        doc = loader_func()
        
        print(f"\n✅ Successfully loaded {plan_name}")
        print(f"Document ID: {doc.document_id}")
        print(f"Plan ID: {doc.plan_id}")
        print(f"Title: {doc.title}")
        print(f"Content Length: {len(doc.content):,} characters")
        print(f"\nFirst 500 characters:\n{doc.content[:500]}...")
        
        return True
    except Exception as e:
        print(f"\n❌ Failed to load {plan_name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*70)
    print("MetLife Plan PDFs Loader Test")
    print("="*70)
    
    # Test FEDVIP
    fedvip_success = test_pdf(load_metlife_fedvip_2025, "FEDVIP 2025")
    
    # Test VADIP
    vadip_success = test_pdf(load_metlife_vadip, "VADIP")
    
    # Summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    print(f"FEDVIP 2025: {'✅ Success' if fedvip_success else '❌ Failed'}")
    print(f"VADIP:       {'✅ Success' if vadip_success else '❌ Failed'}")
    
    if fedvip_success and vadip_success:
        print("\n🎉 All PDFs loaded successfully!")
    else:
        print("\n⚠️  Some PDFs failed to load")
    print("="*70)
