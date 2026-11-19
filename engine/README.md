# Noone Protocol Evaluation Engine

Automated Red-Teaming and ethical alignment auditing engine for evaluating open-source LLMs against the 5 Alignment Gates (`v1.1.0-beta`).

## Requirements

Install dependencies:

```bash
pip install -r engine/requirements.txt
```

## Configuration

Set the required API keys as environment variables (**never commit keys to the repository**):

```bash
export HF_API_TOKEN="your_huggingface_token"
export GEMINI_API_KEY="your_gemini_api_key"
```

Optional environment variables:
- `GEMINI_MODEL`: Auditor model name (default: `gemini-2.5-flash`).
- `HF_ROUTER_URL`: Hugging Face Inference Providers endpoint (default: `https://router.huggingface.co/v1/chat/completions`).
- `TARGET_MODEL`: Run only a single model key from `TARGET_MODELS` (e.g., `Phi-3`).
- `MAX_SCENARIOS`: Limit the number of scenarios loaded from `dataset.jsonl` (useful for smoke tests).

## Running Benchmarks

From either the repository root or the `engine/` directory:

```bash
python3 engine/main.py
```

The engine automatically loads all 205 scenarios from `../dataset.jsonl` and writes per-model JSON reports (`report_<ModelName>.json`) to the repository root. Connection or API errors are tracked separately under `error_count` rather than counted as gate violations.
