# Git Repository Setup Instructions

## Step 1: Initialize Local Git Repository

```powershell
# Navigate to your project directory
cd C:\METCODE\LangChain1

# Initialize git repository
git init

# Add all files to staging
git add .

# Create initial commit
git commit -m "Initial commit: Dental Insurance Chatbot with LangChain, RAG, and MCP"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com
2. Click the '+' icon in the top right corner
3. Select "New repository"
4. Fill in:
   - **Repository name**: `dental-insurance-chatbot` (or your preferred name)
   - **Description**: `Dental insurance member chatbot using LangChain with RAG and MCP concepts`
   - **Visibility**: Choose Public or Private
   - **Do NOT initialize** with README, .gitignore, or license (we already have these)
5. Click "Create repository"

## Step 3: Connect Local Repository to GitHub

After creating the GitHub repository, you'll see a page with setup instructions. Use these commands:

```powershell
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/dental-insurance-chatbot.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Alternative: Using GitHub CLI

If you have GitHub CLI installed:

```powershell
# Create and push repository in one command
gh repo create dental-insurance-chatbot --public --source=. --remote=origin --push
```

## Step 4: Verify Upload

Visit your GitHub repository URL:
```
https://github.com/YOUR_USERNAME/dental-insurance-chatbot
```

## Important Notes

### Files Excluded from Git (in .gitignore)
- `.env` - Contains sensitive API keys (not uploaded)
- `__pycache__/` - Python cache files
- `data/` - Local data including PDFs and vector database
- `*.db`, `*.sqlite` - Database files

### Files Included
- All Python source code
- `.env.example` - Template for environment variables
- `requirements.txt` - Python dependencies
- `README.md` - Documentation
- `.gitignore` - Git ignore rules
- All documentation files (PDF_INTEGRATION.md, etc.)

## What Users Need to Do After Cloning

```powershell
# Clone the repository
git clone https://github.com/YOUR_USERNAME/dental-insurance-chatbot.git
cd dental-insurance-chatbot

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your settings

# Run the chatbot
python main.py
```

## Repository Structure

```
dental-insurance-chatbot/
├── README.md                           # Main documentation
├── requirements.txt                    # Python dependencies
├── .env.example                        # Environment template
├── .gitignore                         # Git ignore rules
├── main.py                            # Application entry point
├── agent.py                           # LangChain agent
├── config.py                          # Configuration management
├── models.py                          # Data models
├── mcp_server.py                      # MCP tools
├── rag_pipeline.py                    # RAG implementation
├── pdf_loader.py                      # PDF processing
├── sample_data.py                     # Sample data
├── test_pdf_loader.py                 # PDF tests
├── test_rag_pdf.py                    # RAG tests
├── test_both_pdfs.py                  # Multi-PDF tests
├── PDF_INTEGRATION.md                 # PDF integration docs
└── METLIFE_PDF_INTEGRATION.md         # MetLife PDF docs
```

## Recommended Repository Settings

### Topics/Tags (Add in GitHub Settings)
- `langchain`
- `rag`
- `chatbot`
- `dental-insurance`
- `llm`
- `openai`
- `azure-openai`
- `python`
- `mcp`
- `chromadb`

### Branch Protection (Optional)
If working with a team:
1. Go to Settings > Branches
2. Add rule for `main` branch
3. Enable "Require pull request reviews before merging"

## Troubleshooting

### Authentication Issues
If you get authentication errors:

**Option 1: HTTPS with Personal Access Token**
```powershell
# Generate token at: https://github.com/settings/tokens
# Use token as password when prompted
```

**Option 2: SSH**
```powershell
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub: https://github.com/settings/keys
# Change remote to SSH
git remote set-url origin git@github.com:YOUR_USERNAME/dental-insurance-chatbot.git
```

### Large Files Warning
If you get warnings about large files (PDFs), they're already in .gitignore. To verify:
```powershell
git status
```

Should not show any PDF files in data/ directory.

## Updating the Repository

After making changes:

```powershell
# Check what changed
git status

# Add changes
git add .

# Commit with message
git commit -m "Description of your changes"

# Push to GitHub
git push
```

## License Recommendation

Consider adding a LICENSE file. Popular options:
- **MIT License** - Permissive, allows commercial use
- **Apache 2.0** - Similar to MIT, includes patent grant
- **GPL-3.0** - Copyleft, requires derivatives to be open source

Create LICENSE file in root directory with your chosen license text.

## Next Steps After Publishing

1. ✅ Add repository description on GitHub
2. ✅ Add topics/tags for discoverability
3. ✅ Enable GitHub Issues for bug tracking
4. ✅ Consider adding GitHub Actions for CI/CD
5. ✅ Star your own repository!
6. ✅ Share with the community

---

**Need help?** Check GitHub's documentation: https://docs.github.com/
