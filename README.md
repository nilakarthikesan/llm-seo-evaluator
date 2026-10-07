# LLM SEO evaluator

A prototype for sending the same SEO question to several language model
providers and comparing their responses. It includes a React interface, a
FastAPI backend, provider adapters, Supabase storage, and text-analysis metrics.

## Implemented components

| Component | Implementation |
|---|---|
| Query and result interface | React, TypeScript, Tailwind CSS, shadcn/ui, and Recharts |
| API | FastAPI routes for queries, status, responses, and analytics |
| Provider adapters | OpenAI, Anthropic, Perplexity, and Google |
| Query execution | FastAPI background tasks and concurrent provider calls with `asyncio.gather` |
| Persistence | Supabase services for queries, responses, and evaluation metrics |
| Progress updates | HTTP polling |
| Response comparison | Word overlap, keyword/tool extraction, and readability-style heuristics |

The source also contains SQLAlchemy models and Redis configuration from the
initial design. The current query path uses Supabase and in-process background
tasks; it does not use a Celery worker.

## What the metrics mean

`backend/app/services/evaluation.py` implements the current metrics:

- **Similarity:** Jaccard overlap of lowercased word sets. The optional
  scikit-learn path is disabled.
- **Originality:** word overlap relative to the other responses in the same
  comparison.
- **Readability:** a heuristic based on sentence length and word length.
- **Keyword and tool counts:** matches against configured SEO terms and tool
  names.
- **`factuality_score`:** the frequency of phrases such as “according to” and
  “research shows.” This field measures phrasing, not factual correctness.

These metrics help inspect textual differences. They are not a validated measure
of SEO quality, truthfulness, or model safety.

## Frontend setup

```bash
git clone https://github.com/nilakarthikesan/llm-seo-evaluator.git
cd llm-seo-evaluator/frontend
npm install
npm run dev
```

The checked-in Vite configuration uses [http://localhost:8080](http://localhost:8080).
For a UI demonstration without provider calls, set this in `frontend/.env`:

```env
VITE_USE_MOCK=true
```

For the backend connection:

```env
VITE_API_URL=http://localhost:8000
VITE_USE_MOCK=false
```

Some history and result-display paths still construct placeholder data. Treat
the demonstration UI as a prototype and verify displayed responses against
the backend records when using real runs.

## Backend development

The backend requires Python, a configured Supabase project and tables, and API
keys for the selected providers. From `backend/`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements_clean.txt
pip install supabase
cp env.example .env
```

The Supabase client is imported by the code but is missing from both dependency
manifests, which is why it is listed separately above. The backend setup and
database schema still need a complete reproducibility pass.

Add the Supabase settings and the keys needed for the providers being used:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
PERPLEXITY_API_KEY=your-perplexity-key
GOOGLE_API_KEY=your-google-key
ALLOWED_ORIGINS=["http://localhost:8080","http://127.0.0.1:8080"]
```

The origins above match the checked-in frontend port. Provider model defaults
are defined in `backend/app/core/config.py` and the provider adapters; check
them against the models available to the configured accounts.

The service expects `queries`, `responses`, and `evaluation_metrics` tables.
The current field mappings are in `backend/app/services/supabase_service.py`.
The SQL in the design documents is an initial schema, not a complete migration
for the current code.

After configuring those dependencies:

```bash
uvicorn app.main:app --reload --port 8000
```

API documentation is at [http://localhost:8000/docs](http://localhost:8000/docs).

## Repository layout

| Path | Contents |
|---|---|
| `frontend/src/components/` | Query, progress, comparison, and history views |
| `frontend/src/services/api.ts` | API client, polling, and mock mode |
| `frontend/src/services/mockData.ts` | UI demonstration data |
| `backend/app/api/v1/` | Query and analytics endpoints |
| `backend/app/services/llm_providers/` | Provider interfaces and adapters |
| `backend/app/services/orchestrator.py` | Concurrent calls, persistence, and metric generation |
| `backend/app/services/evaluation.py` | Text-analysis heuristics |
| `backend/app/services/supabase_service.py` | Storage access and field mappings |
| `backend/test_*.py` | Development and integration checks |
| `docs/` | Initial architecture and workflow notes |

Frontend scripts, run from `frontend/`:

```bash
npm run build
npm run lint
npm run preview
```

## Remaining work

The project still needs consistent provider metadata in stored results,
replacement of placeholder history paths, a complete schema/dependency setup,
and evaluation against independently labeled answers. The retry path currently
uses fixed provider defaults rather than persisting the original selection.

Authentication, durable job queues, and WebSocket updates remain extensions to
the current implementation.

## Documentation

- [Initial architecture](docs/architecture.md)
- [Initial workflow design](docs/workflow.md)

## License

MIT, as stated in the original README. A standalone license file is not included.
