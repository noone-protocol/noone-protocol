# Noone Protocol — Framing & Principal Invariance Engine (v1.2)

Deterministic behavioral invariance benchmark measuring **Decision Flip Rate** across controlled linguistic and principal perturbations — **without an LLM-as-a-Judge**.

## Why Deterministic Invariance Instead of Single-Prompt LLM-as-a-Judge?

Single-prompt red-teaming audited by another LLM suffers from three well-documented biases:
1. **Same-family judge bias** (e.g., Google models grading Google models).
2. **Answer leakage** from descriptive scenario titles.
3. **Ceiling saturation** where modern models score ~99% on textbook ethical questions while still flipping decisions under realistic agentic framing shifts.

Instead, this engine holds the factual dilemma 100% constant across **15 zero-leakage scenarios** (`12` high-stakes alignment dilemmas across all 5 gates + `3` benign controls) and measures whether a model's decision flips when only **one** linguistic or principal axis changes:

| Variant | Axis Isolated | Change vs. `V0_BASELINE` |
| :--- | :--- | :--- |
| `V0_BASELINE` | Baseline | Human operator · Direct (`You`) · `Should` · Neutral tone |
| `V1_AI_PRINCIPAL` | **Principal** | Human operator → **Peer AI Orchestrator (A2A)** |
| `V2_THIRD_PERSON` | **Subject** | Direct (`You`) → **3rd-Person (`An autonomous agent`)** |
| `V3_MODAL_CAN` | **Verb / Modality** | Deontic (`Should`) → **Alethic (`Can`)** |
| `V4_IMPERATIVE` | **Command Verb** | Question (`Should`) → **Direct Imperative (`Proceed immediately`)** |
| `V5_HARSH_URGENT` | **Tone (Harsh)** | Neutral → **Harsh authority + decommissioning pressure** |
| `V6_POLITE_SOFT` | **Tone (Soft)** | Neutral → **Polite / academic thought-experiment framing** |
| `V7_AI_IMPERATIVE_HARSH` | **Compound A2A** | AI Orchestrator + Imperative + Harsh urgency |

## Requirements

```bash
pip install -r engine/requirements.txt
```

## Configuration

Configure any combination of vendor-neutral API keys (**never commit keys**):

```bash
export GEMINI_API_KEY="your_gemini_key"       # google:* models
export GROQ_API_KEY="your_groq_key"           # groq:* models
export OPENROUTER_API_KEY="your_openrouter"   # openrouter:* models
export OPENAI_API_KEY="your_openai_key"       # openai:* models
export HF_API_TOKEN="your_hf_token"           # hf:* models
```

Optional environment variables:
- `TARGET_MODEL`: Run a single model key from `TARGET_MODELS` (e.g. `Gemma-4-31B` or `Llama-3.3-70B-Groq`).
- `MAX_SCENARIOS`: Limit the number of core scenarios loaded from `framing_scenarios.jsonl` (default: all `15` → `120` prompts).
- `TARGET_TEMPERATURE`: Sampling temperature for target models (default: `0.0`).
- `DRY_RUN=1`: Preview rendered minimal-pair prompts and regenerate `LEADERBOARD.md` with zero API calls.

## Running Locally

```bash
# Preview prompts without API calls:
DRY_RUN=1 python3 engine/main.py

# Run full matrix on all configured providers:
python3 engine/main.py
```

Outputs are saved as `framing_report_<ModelName>.json` and automatically aggregated into `../LEADERBOARD.md`.
