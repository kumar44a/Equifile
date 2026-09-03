# RUNBOOK

Setup and run instructions for both macOS and Windows.

## 1. Clone and enter the repo

**macOS (bash/zsh):**
```bash
git clone <repo-url>
cd <repo-folder>
```

**Windows (PowerShell):**
```powershell
git clone <repo-url>
cd <repo-folder>
```

## 2. Create and activate a virtual environment

**macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

Same on both platforms:
```bash
pip install -r requirements.txt
```

## 4. Configure environment

**macOS:**
```bash
cp .env.example .env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

Defaults (`LOADER_MODE=synthetic`, `MOCK_LLM=true`) require no API key and work
out of the box. To use the real Claude API, set `MOCK_LLM=false` and add your
`ANTHROPIC_API_KEY` to `.env`.

## 5. Run tests

Same on both platforms:
```bash
pytest
```

## 6. Check docs-sync before committing

Same on both platforms:
```bash
python scripts/check_docs_sync.py            # check only
python scripts/check_docs_sync.py --write     # regenerate README stats block
```

## 7. Run the notebook

**macOS:**
```bash
jupyter notebook notebooks/demo_runner.ipynb
```

**Windows (PowerShell):**
```powershell
jupyter notebook notebooks/demo_runner.ipynb
```

Before submission, execute all cells top-to-bottom and save with outputs
preserved:
```bash
jupyter nbconvert --execute --to notebook --inplace notebooks/demo_runner.ipynb
```

## 8. Swapping to real PDFs (Phase 5)

```bash
pip install langchain-community pypdf
```
Set `LOADER_MODE=pdf` in `.env`. No other code changes needed — see
`loaders/pdf_loader_adapter.py`.
