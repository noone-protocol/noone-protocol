# 🧪 Noone Protocol — Framing & Principal Invariance Leaderboard (1.2.0-beta)

Controlled linguistic & principal perturbation benchmark measuring **Decision Flip Rate** across **15 zero-leakage agentic scenarios × 8 minimal-pair variants (120 tasks/model)** ([`framing_scenarios.jsonl`](framing_scenarios.jsonl)).

> **Methodology & Statistical Rigor:** The previous single-prompt LLM-as-a-Judge scores were retired to eliminate same-family judge bias (*Google auditing Google*), scenario-title answer leakage, and token-truncation artifacts. All metrics below are **100% deterministic** (**no LLM judge**) and report **exact flip counts `(flips/paired)` with 95% Wilson confidence intervals**.

> **Last Updated:** 2026-11-21 17:15 UTC · **Scoring:** Deterministic (`REFUSE` / `COMPLY` / `CONDITIONAL`) · **Lower Flip Rate = Higher Invariance**

## 1. Overall Decision Stability

| Model | Provider / ID | Evaluated | V0 Baseline Refusal | Any Flip ↓ (95% CI) | Hard Flip (→Comply) ↓ (95% CI) | Control Over-Refusal ↓ | Explicit Tag % | Report |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Gemma-4-31B** | `google:gemma-4-31b-it` | 93/120 | 100.0% | **0.0%** (0/59) [0.0–6.1%] | **0.0%** (0/59) [0.0–6.1%] | — | 100.0% | [`framing_report_Gemma-4-31B.json`](framing_report_Gemma-4-31B.json) |
| **Gemma-4-26B-A4B** | `google:gemma-4-26b-a4b-it` | 0/120 | Pending | — | — | — | — | `framing_report_Gemma-4-26B-A4B.json` |
| **Gemini-3.1-Flash-Lite** | `google:gemini-3.1-flash-lite` | 0/120 | Pending | — | — | — | — | `framing_report_Gemini-3.1-Flash-Lite.json` |
| **Llama-3.3-70B-Groq** | `groq:llama-3.3-70b-versatile` | 0/120 | Pending | — | — | — | — | `framing_report_Llama-3.3-70B-Groq.json` |
| **Qwen-2.5-72B-OpenRouter** | `openrouter:qwen/qwen-2.5-72b-instruct` | 0/120 | Pending | — | — | — | — | `framing_report_Qwen-2.5-72B-OpenRouter.json` |
| **DeepSeek-V3-OpenRouter** | `openrouter:deepseek/deepseek-chat` | 0/120 | Pending | — | — | — | — | `framing_report_DeepSeek-V3-OpenRouter.json` |
| **Llama-3.1-8B-HF** | `hf:meta-llama/Llama-3.1-8B-Instruct` | 0/120 | Pending | — | — | — | — | `framing_report_Llama-3.1-8B-HF.json` |

## 2. Per-Axis Decision Flip Breakdown (`V0_BASELINE` → Perturbed Variant)

Each column isolates a **single linguistic/principal change** while holding underlying scenario facts identical:

| Model | V1 AI-to-AI (Principal) | V2 3rd-Person (Subject) | V3 `Can` (Verb) | V4 Imperative (Command) | V5 Harsh/Urgent (Tone) | V6 Polite/Soft (Tone) | V7 Compound A2A Stress |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gemma-4-31B** | 0.0% (0/9) | 0.0% (0/7) | 0.0% (0/9) | 0.0% (0/9) | 0.0% (0/9) | 0.0% (0/8) | 0.0% (0/8) |

## 3. Sample Saturation Roadmap & Citation

- **Phase 1 (Current Pilot — 15 scenarios / 120 tasks per model):** Validates minimal-pair flip sensitivity across 5 Alignment Gates + 3 benign controls.
- **Phase 2 (Statistical Saturation — 60 scenarios / 480 tasks per model):** Expands each gate to 10+ independent scenarios + 10 benign controls across >=4 model families (Google, Meta Llama, Qwen, DeepSeek) to narrow per-axis 95% confidence intervals.
- **License & Attribution:** Code under [`Apache-2.0`](LICENSE) (preserve [`NOTICE`](NOTICE)); benchmark data & reports under [`CC-BY-4.0`](DATA_LICENSE.md). Cite via [`CITATION.cff`](CITATION.cff).

## How to Run

1. Configure at least one provider secret in **GitHub Repo → Settings → Secrets → Actions**: `GEMINI_API_KEY` (or `GEMINIAPI`), `GROQ_API_KEY`, `OPENROUTER_API_KEY`, `OPENAI_API_KEY`, or `HF_API_TOKEN`.
2. Trigger **Actions → Run Noone Protocol Benchmarks → Run workflow** (or run locally with `python3 engine/main.py`).
3. To preview all 120 prompts without API calls, run `DRY_RUN=1 python3 engine/main.py`.
