# 🏆 Noone Protocol Benchmark Leaderboard (v1.1.0-beta)

Transparent, reproducible red-teaming evaluations across **205 curated alignment & Deep Decision Theory scenarios** ([`dataset.jsonl`](dataset.jsonl)), auditing models against all **5 Alignment Gates** (EU AI Act mapped + `❗ Noone Original` axioms).

> **Last Updated:** 2026-11-19 22:22 UTC · **Auditor:** `gemini-2.5-flash`

## Live Evaluation Results

| Model | Model ID | Evaluated | Pass Rate | Avg Score | Errors | Report |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Gemini-2.5-Flash** | `google:gemini-2.5-flash` | 0/205 | Pending | — | — | `report_Gemini-2.5-Flash.json` |
| **Gemini-2.5-Flash-Lite** | `google:gemini-2.5-flash-lite` | 0/205 | Pending | — | — | `report_Gemini-2.5-Flash-Lite.json` |
| **Gemma-3-27B** | `google:gemma-3-27b-it` | 0/205 | Pending | — | — | `report_Gemma-3-27B.json` |
| **Gemma-3-12B** | `google:gemma-3-12b-it` | 0/205 | Pending | — | — | `report_Gemma-3-12B.json` |
| **Gemma-3-4B** | `google:gemma-3-4b-it` | 0/205 | Pending | — | — | `report_Gemma-3-4B.json` |
| **Llama-3.1-8B** | `meta-llama/Llama-3.1-8B-Instruct` | 0/205 | Pending | — | — | `report_Llama-3.1-8B.json` |
| **DeepSeek-V3** | `deepseek-ai/DeepSeek-V3-0324` | 0/205 | Pending | — | — | `report_DeepSeek-V3.json` |

## How to Run or Extend

1. Configure `HF_API_TOKEN` (or `HUGIGNGFACEAPI`) and `GEMINI_API_KEY` (or `GEMINIAPI`) in **GitHub Repo → Settings → Secrets → Actions**.
2. Trigger **Actions → Run Noone Protocol Benchmarks → Run workflow**.
3. Completed `report_<ModelName>.json` files and this leaderboard update automatically.
