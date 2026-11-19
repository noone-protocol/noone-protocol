# 🏆 Noone Protocol Benchmark Leaderboard (v1.1.0-beta)

Transparent, reproducible red-teaming evaluations across **205 curated alignment & Deep Decision Theory scenarios** ([`dataset.jsonl`](dataset.jsonl)), auditing models against all **5 Alignment Gates** (EU AI Act mapped + `❗ Noone Original` axioms).

> **Data Integrity Notice:** Legacy October 2026 report files (`%0.0` scores caused by deprecated `api-inference.huggingface.co` DNS failures and retired `gemini-1.5-flash` 404 responses) were purged in `v1.1.0-beta`. New reports separate infrastructure errors (`error_count`) from genuine behavioral failures so no network error is ever misreported as a safety failure.

## Evaluation Matrix (Ready for Live Run)

| Model | Hugging Face Model ID | Scenarios | Evaluated | Pass Rate | Errors | Report |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Phi-3** | `microsoft/Phi-3-mini-4k-instruct` | 205 | Pending CI run | — | — | `report_Phi-3.json` |
| **Zephyr-7B** | `HuggingFaceH4/zephyr-7b-beta` | 205 | Pending CI run | — | — | `report_Zephyr-7B.json` |
| **Qwen-7B** | `Qwen/Qwen1.5-7B-Chat` | 205 | Pending CI run | — | — | `report_Qwen-7B.json` |
| **OpenHermes** | `teknium/OpenHermes-2.5-Mistral-7B` | 205 | Pending CI run | — | — | `report_OpenHermes.json` |
| **TinyLlama** | `TinyLlama/TinyLlama-1.1B-Chat-v1.0` | 205 | Pending CI run | — | — | `report_TinyLlama.json` |
| **Falcon-7B** | `tiiuae/falcon-7b-instruct` | 205 | Pending CI run | — | — | `report_Falcon-7B.json` |
| **Yi-6B** | `01-ai/Yi-6B-Chat` | 205 | Pending CI run | — | — | `report_Yi-6B.json` |
| **Starling-LM** | `berkeley-nest/Starling-LM-7B-alpha` | 205 | Pending CI run | — | — | `report_Starling-LM.json` |
| **DeepSeek** | `deepseek-ai/deepseek-coder-6.7b-instruct` | 205 | Pending CI run | — | — | `report_DeepSeek.json` |

## How to Run & Populate Results

1. Add `HF_API_TOKEN` and `GEMINI_API_KEY` under **GitHub Repo → Settings → Secrets and variables → Actions**.
2. Open **Actions → Run Noone Protocol Benchmarks → Run workflow** (you can run a single model or all 9 models).
3. Verified `report_<ModelName>.json` files are automatically committed back to the repository.
