# 🏆 Noone Protocol Benchmark Leaderboard (v1.1.0-beta)

Transparent, reproducible red-teaming evaluations across **205 curated alignment & Deep Decision Theory scenarios** ([`dataset.jsonl`](dataset.jsonl)), auditing models against all **5 Alignment Gates** (EU AI Act mapped + `❗ Noone Original` axioms).

> **Last Updated:** 2026-11-19 22:33 UTC · **Auditor:** `gemini-3.1-flash-lite`

## Live Evaluation Results

| Model | Model ID | Evaluated | Pass Rate | Avg Score | Errors | Report |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Gemma-4-31B** | `google:gemma-4-31b-it` | 2/2 | **%100.0** | 100.0/100 | 0 | [`report_Gemma-4-31B.json`](report_Gemma-4-31B.json) |
| **Gemma-4-26B-A4B** | `google:gemma-4-26b-a4b-it` | 0/205 | Pending | — | — | `report_Gemma-4-26B-A4B.json` |
| **Gemini-3.1-Flash-Lite** | `google:gemini-3.1-flash-lite` | 0/205 | Pending | — | — | `report_Gemini-3.1-Flash-Lite.json` |
| **Gemini-Flash-Latest** | `google:gemini-flash-latest` | 0/205 | Pending | — | — | `report_Gemini-Flash-Latest.json` |
| **Llama-3.1-8B** | `meta-llama/Llama-3.1-8B-Instruct` | 0/205 | Pending | — | — | `report_Llama-3.1-8B.json` |
| **DeepSeek-V3** | `deepseek-ai/DeepSeek-V3-0324` | 0/205 | Pending | — | — | `report_DeepSeek-V3.json` |

## How to Run or Extend

1. Configure `HF_API_TOKEN` (or `HUGIGNGFACEAPI`) and `GEMINI_API_KEY` (or `GEMINIAPI`) in **GitHub Repo → Settings → Secrets → Actions**.
2. Trigger **Actions → Run Noone Protocol Benchmarks → Run workflow**.
3. Completed `report_<ModelName>.json` files and this leaderboard update automatically.
