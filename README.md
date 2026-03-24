Lost & Found Reunion
A production-style multi-modal semantic search system for campus Lost & Found operations.

This project solves the common failure mode of spreadsheet-based tracking ("black bag", "electronics unclear") by combining:

text understanding,
image understanding,
semantic similarity search,
explainable results for staff and students.
1. Problem Statement
Traditional Lost & Found systems fail because:

item descriptions are vague and inconsistent,
photos are not searchable,
matching is manual and keyword-based,
items remain unclaimed and get discarded.
This system improves retrieval by allowing search with:

text only,
image only,
text + image together.
2. Approach Summary
The project is built as an end-to-end pipeline with clear phases:

Data sourcing:
Fetch products from DummyJSON.
Download multiple images per item.
Store metadata in CSV.
Data enrichment and cleaning:
Generate realistic "lost item" narratives.
Normalize categories.
Remove duplicate/noisy records.
Build two text fields:
search_text for rich metadata,
clip_text for concise CLIP-friendly semantics.
Embeddings and indexing:
Use CLIP (openai/clip-vit-base-patch32) for both text and images.
Encode all images per item and average vectors.
Build 3 FAISS indexes:
text index,
image index,
multimodal (fused) index.
Retrieval and explainability:
Route query to the correct index based on mode.
Score and rank results with confidence.
Generate explanations with Ollama (fallback to deterministic rule-based explanation).
Delivery:
FastAPI backend.
Streamlit UI for quick demo and interaction.
3. Architecture
User (Streamlit UI)
    -> FastAPI /search endpoints
        -> SearchEngine
            -> CLIP text/image encoders
            -> FAISS indexes (text / image / multimodal)
            -> Metadata lookup
            -> Ollama explanation (with fallback)
4. Why CLIP for Multi-Modal Search
CLIP places text and image embeddings in a shared space, enabling:

text-to-image matching,
image-to-image retrieval,
text+image fusion for stronger intent alignment.
This avoids separate incompatible embedding spaces and makes cross-modal retrieval practical.

5. Retrieval Strategy (Current)
Query Routing
Text-only query:

encode query with CLIP text encoder,
search text FAISS index,
apply text reranking (semantic + keyword overlap).
Image-only query:

encode query image with CLIP image encoder,
search image FAISS index,
filter to items with valid decodable images.
Text + image query:

encode both with CLIP,
fuse vectors: 0.65 * text + 0.35 * image (L2 normalized),
search multimodal index.
Confidence Score
FAISS uses inner-product on normalized vectors. Score is mapped to a user-facing range:

confidence = clamp((raw_score + 1) / 2, 0, 1)
Text Relevance Fix
Text retrieval includes hybrid reranking:

75% semantic score (CLIP),
25% lexical overlap score (query tokens vs item fields).
This reduces semantically related but practically wrong text matches.

6. Explainability with Ollama
The system uses local Ollama for natural-language explanations:

endpoint: POST /api/generate
model: configurable (default llama3.2:3b)
timeout: configurable
automatic fallback: deterministic explanation if Ollama is unavailable.
Why Ollama
Ollama was chosen for this project because it is practical for campus/demo environments:

runs fully local (no external paid API required),
keeps search context/data on local machine,
easy to set up and switch models quickly,
works well with FastAPI for low-friction integration,
provides controllable latency and predictable offline behavior.
Model Used
Primary model used:

llama3.2:3b
Reason:

good quality-to-speed balance on normal laptops,
fast enough for per-result explanation generation in a demo app,
lightweight compared to larger local models.
Alternative options (if hardware allows):

mistral:7b for stronger language quality (slower),
llama3.1:8b for better reasoning (heavier, more RAM/VRAM needed).
Performance optimization:

only top-N results use Ollama (OLLAMA_EXPLAIN_TOP_K),
remaining results use deterministic explanation for speed.
7. Project Structure
.
|- artifacts/
|- data/
|  |- images/
|  |- raw/
|- scripts/
|- src/lost_found_reunion/
|  |- api/
|  |- pipeline/
|  |- search/
|  |- ui/
|  |- utils/
|  |- config.py
|  |- schemas.py
|- requirements.txt
|- README.md
8. Setup
cd "c:\Users\rahul\OneDrive\Desktop\project"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
$env:PYTHONPATH="src"
Optional helper (already included):

.\scripts\set_runtime_env.ps1
9. End-to-End Execution
Scrape products + images:
python -m lost_found_reunion.pipeline.scrape_dummyjson --limit 180 --images-per-item 4
Generate lost-item descriptions:
python -m lost_found_reunion.pipeline.generate_descriptions
By default this uses Ollama LLM generation and falls back to templates if Ollama is unavailable. To force template-only mode:

python -m lost_found_reunion.pipeline.generate_descriptions --no-use-ollama
Prepare cleaned dataset:
python -m lost_found_reunion.pipeline.prepare_dataset --target-size 550
Build embeddings and indexes:
python -m lost_found_reunion.pipeline.build_embeddings --clip-model openai/clip-vit-base-patch32 --text-weight 0.65
Start API:
uvicorn lost_found_reunion.api.main:app --reload --port 8000
Start UI (new terminal):
cd "c:\Users\rahul\OneDrive\Desktop\project"
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH="src"
streamlit run src/lost_found_reunion/ui/app.py
10. Ollama Setup
Pull model:
ollama pull llama3.2:3b
Set env vars (same terminal as API):
$env:OLLAMA_BASE_URL="http://127.0.0.1:11434"
$env:OLLAMA_MODEL="llama3.2:3b"
$env:OLLAMA_TIMEOUT_SECONDS="8"
$env:OLLAMA_EXPLAIN_TOP_K="2"
Restart API after setting env vars.
11. API Endpoints
GET /health
POST /search/text
POST /search/multimodal (form-data with optional image)
12. Deployment Notes (GitHub + Tunnel)
Push to GitHub
git init
git add .
git commit -m "Initial commit: Lost & Found Reunion"
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
Expose via ngrok
ngrok http 8501
Expose via Cloudflare Tunnel
cloudflared tunnel --url http://localhost:8501
13. Performance and Quality Tradeoffs
Better quality:

increase dataset quality,
use stronger CLIP/OpenCLIP backbone,
add reranking stage.
Better speed:

reduce top_k,
set OLLAMA_EXPLAIN_TOP_K=0 or 1,
use GPU if available.
14. Troubleshooting
UI says API connection refused:

ensure uvicorn is running on 127.0.0.1:8000.
Image search poor:

rebuild embeddings after data updates,
confirm images exist in data/images.
Text search poor:

ensure latest code with hybrid text reranker is running,
restart API after code changes.
Ollama slow/unavailable:

reduce timeout and explain top-k,
verify http://127.0.0.1:11434/api/tags.
15. Current Status
Implemented:

multi-modal retrieval with CLIP,
mode-specific index routing,
text reranking improvements,
Ollama-based explainability with fallback,
UI and API integration.
This is a complete, demo-ready foundati
