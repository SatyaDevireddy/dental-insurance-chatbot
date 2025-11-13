# Adding PDF Documents to the Chatbot

## Overview

The chatbot can now load and query PDF documents! The MetLife FEDVIP 2025 Dental Plan Summary has been integrated into the RAG pipeline.

## How It Works

1. **PDF Download**: The system downloads the PDF from the URL
2. **Text Extraction**: Extracts text from all pages using PyPDF
3. **Vector Storage**: Splits the text into chunks and stores them in ChromaDB
4. **Semantic Search**: Users can query the document using natural language

## Already Added

✅ **MetLife FEDVIP 2025 Dental Plan Summary**

- Source: https://fedvip.metlife.com/content/dam/metlifecom/us/homepage/federal-dental/2024/pdf/plan-summary/MetLife_FEDVIP_2025-Dental_Web_Summary.pdf
- Pages: 10
- Content: 20,600+ characters
- Covers: Plan highlights, covered services, benefits options, rates, enrollment info

## Example Queries

Users can now ask questions like:

- "What are the rates for the MetLife FEDVIP plan?"
- "What dental services are covered under the FEDVIP plan?"
- "Tell me about the MetLife federal dental plan benefits"
- "What are the enrollment dates for FEDVIP?"
- "What's the coverage percentage for routine services?"
- "Are there any savings with the MetLife federal plan?"

## Adding More PDFs

To add additional PDF documents, follow these steps:

### Method 1: Using the pdf_loader module

```python
from pdf_loader import load_pdf_as_plan_document
from rag_pipeline import RAGPipeline

# Initialize RAG pipeline
rag = RAGPipeline()

# Load your PDF
doc = load_pdf_as_plan_document(
    url="https://example.com/your-document.pdf",
    document_id="DOC_YOUR_ID",
    plan_id="YOUR_PLAN_ID",
    document_type="policy",  # or "benefits_summary", "faq", etc.
    title="Your Document Title",
    save_local=True
)

# Add to RAG pipeline
rag.add_documents([doc])
```

### Method 2: Create a custom loader function

Edit `pdf_loader.py` and add a new function:

```python
def load_your_custom_pdf() -> PlanDocument:
    """Load your custom PDF document."""
    url = "https://your-url.com/document.pdf"

    return load_pdf_as_plan_document(
        url=url,
        document_id="DOC_CUSTOM_001",
        plan_id="CUSTOM_PLAN",
        document_type="plan_summary",
        title="Your Custom Document",
        save_local=True
    )
```

Then import and use it in `main.py`:

```python
from pdf_loader import load_your_custom_pdf

# In initialize_system() function:
try:
    custom_doc = load_your_custom_pdf()
    rag_pipeline.add_documents([custom_doc])
    print("✅ Custom PDF loaded")
except Exception as e:
    print(f"⚠️  Warning: Could not load custom PDF: {str(e)}")
```

## Testing PDF Loading

Test any PDF loading with:

```powershell
python test_pdf_loader.py
```

## Supported Document Types

- `policy` - Insurance policies
- `benefits_summary` - Benefits summary documents
- `plan_summary` - Plan overview documents
- `faq` - Frequently asked questions
- `provider_directory` - Provider listings
- `coverage_guide` - Coverage guidelines
- `enrollment_guide` - Enrollment instructions

## Local PDF Storage

Downloaded PDFs are saved to:

```
./data/pdfs/
```

This allows the system to avoid re-downloading on subsequent runs.

## Technical Details

### PDF Processing

- **Library**: PyPDF (pypdf)
- **Encoding**: UTF-8
- **Page extraction**: Sequential

### Vector Storage

- **Database**: ChromaDB
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Chunk size**: 1000 characters
- **Chunk overlap**: 200 characters

### Metadata Stored

Each PDF chunk includes:

- `document_id`
- `plan_id`
- `document_type`
- `title`
- `last_updated`

## Troubleshooting

### PDF Download Fails

- Check internet connection
- Verify the URL is accessible
- Some sites may block automated downloads - try downloading manually and loading from file

### Text Extraction Issues

- Some PDFs have text embedded as images (scanned documents)
- For image-based PDFs, you'll need OCR (Optical Character Recognition)
- Consider using `pdf2image` + `pytesseract` for scanned documents

### Memory Issues

- Large PDFs may require significant memory
- Process in batches if needed
- Adjust chunk size in `rag_pipeline.py` if needed

## Future Enhancements

Possible improvements:

1. Add OCR support for scanned PDFs
2. Support for other formats (Word, Excel, etc.)
3. Automatic URL monitoring for document updates
4. Multi-language support
5. Table extraction and structured data parsing
