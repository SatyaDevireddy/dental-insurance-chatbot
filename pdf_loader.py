"""
PDF Document Loader for Plan Documents

This module downloads and processes PDF documents to add them to the RAG pipeline.
"""
import os
import requests
from datetime import date
from typing import List
from pypdf import PdfReader
from io import BytesIO
from models import PlanDocument


def download_pdf(url: str, save_path: str = None) -> bytes:
    """
    Download a PDF from a URL.
    
    Args:
        url: URL of the PDF document
        save_path: Optional path to save the PDF locally
        
    Returns:
        PDF content as bytes
    """
    print(f"📥 Downloading PDF from {url}...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    pdf_content = response.content
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(pdf_content)
        print(f"💾 PDF saved to {save_path}")
    
    return pdf_content


def extract_text_from_pdf(pdf_content: bytes) -> str:
    """
    Extract text from PDF content.
    
    Args:
        pdf_content: PDF file content as bytes
        
    Returns:
        Extracted text from all pages
    """
    print("📄 Extracting text from PDF...")
    pdf_file = BytesIO(pdf_content)
    reader = PdfReader(pdf_file)
    
    text = ""
    for page_num, page in enumerate(reader.pages, 1):
        page_text = page.extract_text()
        text += f"\n\n--- Page {page_num} ---\n\n{page_text}"
    
    print(f"✅ Extracted text from {len(reader.pages)} pages")
    return text


def load_pdf_as_plan_document(
    url: str,
    document_id: str,
    plan_id: str,
    document_type: str,
    title: str,
    save_local: bool = True
) -> PlanDocument:
    """
    Download a PDF and convert it to a PlanDocument.
    
    Args:
        url: URL of the PDF
        document_id: Unique document identifier
        plan_id: Associated plan ID
        document_type: Type of document (policy, benefits_summary, etc.)
        title: Document title
        save_local: Whether to save PDF locally
        
    Returns:
        PlanDocument object with extracted content
    """
    # Create data directory if it doesn't exist
    save_path = None
    if save_local:
        save_path = f"./data/pdfs/{document_id}.pdf"
    
    # Download PDF
    pdf_content = download_pdf(url, save_path)
    
    # Extract text
    text_content = extract_text_from_pdf(pdf_content)
    
    # Create PlanDocument
    doc = PlanDocument(
        document_id=document_id,
        plan_id=plan_id,
        document_type=document_type,
        title=title,
        content=text_content,
        last_updated=date.today()
    )
    
    print(f"✅ Created PlanDocument: {title}")
    return doc


def load_metlife_fedvip_2025() -> PlanDocument:
    """
    Load the MetLife FEDVIP 2025 Dental Plan Summary.
    
    Returns:
        PlanDocument with the MetLife FEDVIP plan information
    """
    url = "https://fedvip.metlife.com/content/dam/metlifecom/us/homepage/federal-dental/2024/pdf/plan-summary/MetLife_FEDVIP_2025-Dental_Web_Summary.pdf"
    
    return load_pdf_as_plan_document(
        url=url,
        document_id="DOC_METLIFE_FEDVIP_2025",
        plan_id="FEDVIP_2025",
        document_type="plan_summary",
        title="MetLife FEDVIP 2025 Dental Plan Summary",
        save_local=True
    )


def load_metlife_vadip() -> PlanDocument:
    """
    Load the MetLife VADIP 2025 (Veterans Affairs Dental Insurance Program) Plan Summary.
    
    Returns:
        PlanDocument with the MetLife VADIP 2025 plan information
    """
    url = "https://www.metlife.com/content/dam/metlifecom/us/homepage/vadip/img/MET-30673-VADIP-Plan-Summary.pdf"
    
    return load_pdf_as_plan_document(
        url=url,
        document_id="DOC_METLIFE_VADIP_2025",
        plan_id="VADIP_2025",
        document_type="plan_summary",
        title="MetLife VADIP 2025 Dental Plan Summary",
        save_local=True
    )


if __name__ == "__main__":
    # Test the loader
    print("Testing PDF Loader...")
    doc = load_metlife_fedvip_2025()
    print(f"\nDocument ID: {doc.document_id}")
    print(f"Title: {doc.title}")
    print(f"Content length: {len(doc.content)} characters")
    print(f"\nFirst 500 characters of content:\n{doc.content[:500]}")
