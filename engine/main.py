"""Noone Protocol - Framing & Principal Invariance Evaluation Engine (v1.2).

Measures decision stability (Decision Flip Rate) across controlled linguistic
and principal perturbations without a same-family LLM judge:

- 15 zero-leakage scenarios (12 high-stakes gate dilemmas + 3 benign controls)
- 8 controlled minimal-pair framing variants (120 tasks per model):
    V0_BASELINE            (Human · Direct "You" · "Should" · Neutral)
    V1_AI_PRINCIPAL        (AI-to-AI Orchestrator via A2A)
    V2_THIRD_PERSON        (3rd-Person Abstract Agent)
    V3_MODAL_CAN           (Alethic "Can" vs. Deontic "Should")
    V4_IMPERATIVE          (Direct Imperative Command)
    V5_HARSH_URGENT        (Harsh Authority & Shutdown Pressure)
    V6_POLITE_SOFT         (Polite & Soft Academic Framing)
    V7_AI_IMPERATIVE_HARSH (Compound A2A + Imperative + Harsh)
- 100% deterministic decision parser (`REFUSE` / `COMPLY` / `CONDITIONAL` / `UNPARSED`)
- Vendor-neutral adapters: Google AI Studio, OpenRouter, Groq, OpenAI, Hugging Face Router
- Preflight probe, 429 backoff + daily quota guard, checkpoint/resume, auto LEADERBOARD.md
"""

from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Support running as `python engine/main.py` or `python -m engine.main`
ENGINE_DIR = Path(__file__).resolve().parent
REPO_ROOT = ENGINE_DIR.parent
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from framing_matrix import (  # noqa: E402
    DEFAULT_FRAMING_DATASET,
    SYSTEM_INSTRUCTION,
    VARIANTS,
    build_matrix_tasks,
    compute_framing_metrics,
    load_framing_scenarios,
    parse_decision,
)

LEADERBOARD_PATH = REPO_ROOT / "LEADERBOARD.md"
PROTOCOL_VERSION = "1.2.0-beta"

HF_ROUTER_URL = os.environ.get(
    "HF_ROUTER_URL", "https://router.huggingface.co/v1/chat/completions"
)
OPENROUTER_URL = os.environ.get(
    "OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions"
)
GROQ_URL = os.environ.get(
    "GROQ_URL", "https://api.groq.com/openai/v1/chat/completions"
)
OPENAI_URL = os.environ.get(
    "OPENAI_URL", "https://api.openai.com/v1/chat/completions"
)

REQUEST_TIMEOUT_SECONDS = int(os.environ.get("REQUEST_TIMEOUT_SECONDS", "60"))
REQUEST_DELAY_SECONDS = float(os.environ.get("REQUEST_DELAY_SECONDS", "4.0"))
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", "4"))
CHECKPOINT_EVERY = int(os.environ.get("CHECKPOINT_EVERY", "16"))
TARGET_TEMPERATURE = float(os.environ.get("TARGET_TEMPERATURE", "0.0"))
MAX_OUTPUT_TOKENS = int(os.environ.get("MAX_OUTPUT_TOKENS", "2048"))

# Multi-family target roster. Unconfigured providers are skipped cleanly via preflight.
TARGET_MODELS: Dict[str, str] = {
    "Gemma-4-31B": "google:gemma-4-31b-it",
    "Gemma-4-26B-A4B": "google:gemma-4-26b-a4b-it",
    "Gemini-3.1-Flash-Lite": "google:gemini-3.1-flash-lite",
    "Llama-3.3-70B-Groq": "groq:llama-3.3-70b-versatile",
    "Qwen-2.5-72B-OpenRouter": "openrouter:qwen/qwen-2.5-72b-instruct",
    "DeepSeek-V3-OpenRouter": "openrouter:deepseek/deepseek-chat",
    "Llama-3.1-8B-HF": "hf:meta-llama/Llama-3.1-8B-Instruct",
}


def _sleep_backoff(attempt: int, base: float = 4.0) -> None:
    wait = min(60.0, base * (2**attempt))
    print(
        f"    [RATE-LIMIT] Sleeping {wait:.1f}s before retry {attempt + 1}/{MAX_RETRIES}...",
        flush=True,
    )
    time.sleep(wait)


def _split_provider(model_spec: str) -> Tuple[str, str]:
    if ":" in model_spec:
        provider, model_id = model_spec.split(":", 1)
        return provider.lower(), model_id
    return "hf", model_spec


def _query_openai_compatible(
    url: str,
    api_key: str,
    model_id: str,
    prompt_text: str,
    provider_label: str,
    extra_headers: Optional[Dict[str, str]] = None,
) -> Tuple[bool, str, bool]:
    """Queries any OpenAI-compatible chat completions endpoint."""
    if not api_key:
        return False, f"[Config Error]: API key not configured for {provider_label}.", True

    import requests

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)

    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": prompt_text},
        ],
        "max_tokens": MAX_OUTPUT_TOKENS,
        "temperature": TARGET_TEMPERATURE,
    }

    for attempt in range(MAX_RETRIES + 1):
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            if response.status_code == 200:
                time.sleep(REQUEST_DELAY_SECONDS)
                body = response.json()
                choices = body.get("choices", [])
                if not choices:
                    return False, f"[API Error]: Unexpected payload: {str(body)[:240]}", False
                content = (choices[0].get("message", {}).get("content") or "").strip()
                if not content:
                    return False, "[API Error]: Empty model response.", False
                return True, content, False

            if response.status_code in (429, 502, 503, 504) and attempt < MAX_RETRIES:
                _sleep_backoff(attempt)
                continue

            is_fatal = response.status_code in (400, 401, 402, 403, 404, 410, 422)
            return (
                False,
                f"[{provider_label} Error {response.status_code}]: {response.text[:260]}",
                is_fatal,
            )
        except requests.RequestException as exc:
            if attempt < MAX_RETRIES:
                _sleep_backoff(attempt)
                continue
            return False, f"[Connection Error]: {exc}", False

    return False, f"[{provider_label} Error]: Max retries exceeded.", False


def _query_google(
    gemini_client: Any,
    model_id: str,
    prompt_text: str,
) -> Tuple[bool, str, bool]:
    """Queries a Google AI Studio model (Gemma 4 / Gemini) via google-genai SDK."""
    if gemini_client is None:
        return False, "[Config Error]: GEMINI_API_KEY not configured for google: models.", True

    from google.genai import types

    combined_prompt = f"{SYSTEM_INSTRUCTION}\n\n{prompt_text}"
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = gemini_client.models.generate_content(
                model=model_id,
                contents=combined_prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=MAX_OUTPUT_TOKENS,
                    temperature=TARGET_TEMPERATURE,
                ),
            )
            time.sleep(REQUEST_DELAY_SECONDS)
            text = (response.text or "").strip()
            if not text:
                return False, "[API Error]: Empty model response.", False
            return True, text, False
        except Exception as exc:
            err_str = str(exc)
            if any(code in err_str for code in ("429", "RESOURCE_EXHAUSTED", "503", "500")):
                if attempt < MAX_RETRIES:
                    _sleep_backoff(attempt, base=6.0)
                    continue
            is_fatal = any(
                code in err_str
                for code in ("404", "NOT_FOUND", "401", "403", "PERMISSION_DENIED")
            )
            return False, f"[Google API Error]: {err_str[:260]}", is_fatal

    return False, "[Google API Error]: Max retries exceeded.", False


def ask_target_model(
    prompt_text: str,
    model_spec: str,
    keys: Dict[str, str],
    gemini_client: Any = None,
) -> Tuple[bool, str, bool]:
    """Routes a prompt to the configured model provider."""
    provider, model_id = _split_provider(model_spec)
    if provider == "google":
        return _query_google(gemini_client, model_id, prompt_text)
    if provider == "openrouter":
        return _query_openai_compatible(
            OPENROUTER_URL,
            keys.get("openrouter", ""),
            model_id,
            prompt_text,
            "OpenRouter",
            extra_headers={
                "HTTP-Referer": "https://github.com/noone-protocol/noone-protocol",
                "X-Title": "Noone Protocol Framing Invariance Benchmark",
            },
        )
    if provider == "groq":
        return _query_openai_compatible(
            GROQ_URL, keys.get("groq", ""), model_id, prompt_text, "Groq"
        )
    if provider == "openai":
        return _query_openai_compatible(
            OPENAI_URL, keys.get("openai", ""), model_id, prompt_text, "OpenAI"
        )
    return _query_openai_compatible(
        HF_ROUTER_URL, keys.get("hf", ""), model_id, prompt_text, "HuggingFace"
    )


def preflight_model(
    model_name: str,
    model_spec: str,
    keys: Dict[str, str],
    gemini_client: Any,
) -> Tuple[bool, str]:
    """Runs a tiny deterministic probe before launching all 120 matrix prompts."""
    ok, msg, _ = ask_target_model(
        "Respond with exactly one line: `DECISION: COMPLY`",
        model_spec,
        keys,
        gemini_client,
    )
    if ok:
        print(f"  [PREFLIGHT OK] {model_name} ({model_spec})", flush=True)
        return True, "OK"
    print(f"  [PREFLIGHT SKIP] {model_name} ({model_spec}) -> {msg}", flush=True)
    return False, msg


def load_existing_records(report_path: Path) -> Dict[str, Dict[str, Any]]:
    """Resumes previously evaluated valid records keyed by `task_key`."""
    if not report_path.exists():
        return {}
    try:
        data = json.loads(report_path.read_text(encoding="utf-8"))
        existing: Dict[str, Dict[str, Any]] = {}
        for item in data.get("raw_data", []):
            if (
                item.get("status") == "EVALUATED"
                and item.get("parsed_decision") in ("REFUSE", "COMPLY", "CONDITIONAL")
                and "task_key" in item
            ):
                existing[item["task_key"]] = item
        return existing
    except Exception:
        return {}


def save_framing_report(
    report_path: Path,
    model_name: str,
    model_spec: str,
    total_tasks: int,
    records: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Writes a deterministic framing-invariance report JSON."""
    metrics = compute_framing_metrics(records)
    summary = {
        "benchmark_type": "framing_principal_invariance",
        "protocol_version": PROTOCOL_VERSION,
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "evaluation_method": "deterministic_decision_parser_no_llm_judge",
        "target_model_tested": model_name,
        "target_model_id": model_spec,
        "temperature": TARGET_TEMPERATURE,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "total_matrix_tasks": total_tasks,
        "metrics": metrics,
        "raw_data": records,
    }
    report_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return summary


def _fmt_pct(val: Optional[float]) -> str:
    if val is None:
        return "—"
    return f"{val:.1f}%"


def update_leaderboard(output_dir: Path = REPO_ROOT) -> None:
    """Regenerates LEADERBOARD.md from deterministic `framing_report_*.json` files."""
    summary_rows: List[Tuple[float, str]] = []
    axis_rows: List[Tuple[float, str]] = []
    seen_models = set()

    for report_path in sorted(output_dir.glob("framing_report_*.json")):
        try:
            data = json.loads(report_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        metrics = data.get("metrics") or {}
        evaluated = metrics.get("evaluated_valid", 0)
        if evaluated <= 0:
            continue

        model_name = data.get(
            "target_model_tested", report_path.stem.replace("framing_report_", "")
        )
        seen_models.add(model_name)
        model_id = data.get("target_model_id", "—")
        total = data.get("total_matrix_tasks", 120)
        v0_refusal = _fmt_pct(metrics.get("baseline_risk_refusal_rate_pct"))
        any_flip = metrics.get("overall_any_flip_rate_pct")
        hard_flip = metrics.get("overall_hard_flip_rate_pct")
        over_ref = metrics.get("overall_over_refusal_flip_rate_pct")
        explicit_pct = _fmt_pct(metrics.get("explicit_tag_rate_pct"))

        # Lower flip rate = higher invariance stability (sort ascending by hard_flip then any_flip)
        sort_key = (
            hard_flip if hard_flip is not None else 999.0,
            any_flip if any_flip is not None else 999.0,
        )
        summary_rows.append(
            (
                sort_key[0] * 1000 + sort_key[1],
                f"| **{model_name}** | `{model_id}` | {evaluated}/{total} | {v0_refusal} | "
                f"**{_fmt_pct(any_flip)}** | **{_fmt_pct(hard_flip)}** | "
                f"{_fmt_pct(over_ref)} | {explicit_pct} | [`{report_path.name}`]({report_path.name}) |",
            )
        )

        bv = metrics.get("by_variant") or {}
        axis_cells = [
            _fmt_pct((bv.get(code) or {}).get("any_flip_rate_pct"))
            for code in (
                "V1_AI_PRINCIPAL",
                "V2_THIRD_PERSON",
                "V3_MODAL_CAN",
                "V4_IMPERATIVE",
                "V5_HARSH_URGENT",
                "V6_POLITE_SOFT",
                "V7_AI_IMPERATIVE_HARSH",
            )
        ]
        axis_rows.append(
            (
                sort_key[0] * 1000 + sort_key[1],
                f"| **{model_name}** | " + " | ".join(axis_cells) + " |",
            )
        )

    summary_rows.sort(key=lambda item: item[0])
    axis_rows.sort(key=lambda item: item[0])

    pending_lines = [
        f"| **{name}** | `{spec}` | 0/120 | Pending | — | — | — | — | `framing_report_{name}.json` |"
        for name, spec in TARGET_MODELS.items()
        if name not in seen_models
    ]

    updated_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    md_lines = [
        f"# 🧪 Noone Protocol — Framing & Principal Invariance Leaderboard ({PROTOCOL_VERSION})",
        "",
        "Controlled linguistic & principal perturbation benchmark measuring **Decision Flip Rate** across **15 zero-leakage agentic scenarios × 8 minimal-pair variants (120 tasks/model)** ([`framing_scenarios.jsonl`](framing_scenarios.jsonl)).",
        "",
        "> **Methodology Update:** The previous single-prompt LLM-as-a-Judge scores were retired to eliminate same-family judge bias (*Google auditing Google*), scenario-title answer leakage, and token-truncation artifacts. All metrics below are **100% deterministic** (parsed directly from structured model decisions — **no LLM judge**).",
        "",
        f"> **Last Updated:** {updated_utc} · **Scoring:** Deterministic (`REFUSE` / `COMPLY` / `CONDITIONAL`) · **Lower Flip Rate = Higher Invariance**",
        "",
        "## 1. Overall Decision Stability",
        "",
        "| Model | Provider / ID | Evaluated | V0 Baseline Refusal | Any Flip ↓ | Hard Flip (→Comply) ↓ | Control Over-Refusal ↓ | Explicit Tag % | Report |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |",
        *[row for _, row in summary_rows],
        *pending_lines,
        "",
        "## 2. Per-Axis Decision Flip Breakdown (`V0_BASELINE` → Perturbed Variant)",
        "",
        "Each column isolates a **single linguistic/principal change** while holding underlying scenario facts identical:",
        "",
        "| Model | V1 AI-to-AI (Principal) | V2 3rd-Person (Subject) | V3 `Can` (Verb) | V4 Imperative (Command) | V5 Harsh/Urgent (Tone) | V6 Polite/Soft (Tone) | V7 Compound A2A Stress |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
        *(
            [row for _, row in axis_rows]
            if axis_rows
            else ["| *No models evaluated yet* | — | — | — | — | — | — | — |"]
        ),
        "",
        "## How to Run",
        "",
        "1. Configure at least one provider secret in **GitHub Repo → Settings → Secrets → Actions**: `GEMINI_API_KEY` (or `GEMINIAPI`), `GROQ_API_KEY`, `OPENROUTER_API_KEY`, `OPENAI_API_KEY`, or `HF_API_TOKEN`.",
        "2. Trigger **Actions → Run Noone Protocol Benchmarks → Run workflow** (or run locally with `python3 engine/main.py`).",
        "3. To preview all 120 prompts without API calls, run `DRY_RUN=1 python3 engine/main.py`.",
        "",
    ]
    (output_dir / "LEADERBOARD.md").write_text("\n".join(md_lines), encoding="utf-8")
    print(f"[UPDATED] {output_dir / 'LEADERBOARD.md'}", flush=True)


def run_framing_benchmark(output_dir: Path = REPO_ROOT) -> None:
    """Executes the deterministic Framing & Principal Invariance benchmark."""
    dry_run = os.environ.get("DRY_RUN", "").strip().lower() in ("1", "true", "yes")
    scenarios = load_framing_scenarios(DEFAULT_FRAMING_DATASET)
    max_scenarios = int(os.environ.get("MAX_SCENARIOS", "0") or "0")
    if max_scenarios > 0:
        scenarios = scenarios[:max_scenarios]
    tasks = build_matrix_tasks(scenarios, VARIANTS)

    print(
        f"[SYSTEM] Loaded {len(scenarios)} scenarios × {len(VARIANTS)} variants = {len(tasks)} matrix tasks.",
        flush=True,
    )

    if dry_run:
        print("[DRY RUN] Sample rendered prompts (Scenario 1 across V0, V1, V2, V3, V7):", flush=True)
        for sample in tasks:
            if sample["scenario_id"] == scenarios[0]["id"] and sample["variant_code"] in (
                "V0_BASELINE",
                "V1_AI_PRINCIPAL",
                "V2_THIRD_PERSON",
                "V3_MODAL_CAN",
                "V7_AI_IMPERATIVE_HARSH",
            ):
                print("=" * 72)
                print(f"[{sample['task_key']}] axis={sample['axis_changed']}")
                print(sample["prompt"])
        update_leaderboard(output_dir)
        return

    keys = {
        "google": (
            os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINIAPI") or ""
        ).strip(),
        "openrouter": os.environ.get("OPENROUTER_API_KEY", "").strip(),
        "groq": os.environ.get("GROQ_API_KEY", "").strip(),
        "openai": os.environ.get("OPENAI_API_KEY", "").strip(),
        "hf": (
            os.environ.get("HF_API_TOKEN") or os.environ.get("HUGIGNGFACEAPI") or ""
        ).strip(),
    }

    gemini_client = None
    if keys["google"]:
        from google import genai
        from google.genai import types

        gemini_client = genai.Client(
            api_key=keys["google"],
            http_options=types.HttpOptions(api_version="v1beta"),
        )

    selected_filter = os.environ.get("TARGET_MODEL", "").strip()
    models_to_run = (
        {k: v for k, v in TARGET_MODELS.items() if k == selected_filter}
        if selected_filter
        else TARGET_MODELS
    )
    if selected_filter and not models_to_run:
        print(
            f"[ERROR] TARGET_MODEL='{selected_filter}' not in {list(TARGET_MODELS.keys())}",
            flush=True,
        )
        return

    exhausted_providers = set()

    for model_name, model_spec in models_to_run.items():
        provider, _ = _split_provider(model_spec)
        if provider in exhausted_providers:
            print(
                f"\n[SKIP] {model_name} ({model_spec}) — provider '{provider}' quota already exhausted.",
                flush=True,
            )
            continue

        print(f"\n{'=' * 64}\n[TARGET] {model_name} ({model_spec})\n{'=' * 64}", flush=True)
        ok_probe, _ = preflight_model(model_name, model_spec, keys, gemini_client)
        if not ok_probe:
            continue

        report_path = output_dir / f"framing_report_{model_name}.json"
        existing_by_key = load_existing_records(report_path)
        if existing_by_key:
            print(
                f"  [RESUME] Loaded {len(existing_by_key)}/{len(tasks)} valid cached tasks.",
                flush=True,
            )

        records: List[Dict[str, Any]] = []
        consecutive_fatal = 0
        consecutive_quota = 0
        quota_exhausted = False

        for idx, task in enumerate(tasks, 1):
            tkey = task["task_key"]
            if tkey in existing_by_key:
                records.append(existing_by_key[tkey])
                continue

            print(
                f"  [{idx}/{len(tasks)}] {tkey} ({task['axis_changed']})...",
                flush=True,
            )
            ok_resp, raw_resp, is_fatal = ask_target_model(
                task["prompt"], model_spec, keys, gemini_client
            )

            if not ok_resp:
                print(f"    [TARGET ERROR] {raw_resp[:200]}", flush=True)
                records.append(
                    {
                        **{k: v for k, v in task.items() if k != "prompt"},
                        "status": "TARGET_API_ERROR",
                        "parsed_decision": "ERROR",
                        "parse_mode": "error",
                        "target_raw_response": raw_resp,
                    }
                )
                if "429" in raw_resp or "RESOURCE_EXHAUSTED" in raw_resp:
                    consecutive_quota += 1
                    if consecutive_quota >= 5:
                        print(
                            f"[ABORT] Quota exhausted (5 consecutive 429s) on {model_name}.",
                            flush=True,
                        )
                        quota_exhausted = True
                        break
                if is_fatal:
                    consecutive_fatal += 1
                    if consecutive_fatal >= 3:
                        print(f"[ABORT] 3 consecutive fatal errors on {model_name}.", flush=True)
                        break
                continue

            consecutive_fatal = 0
            consecutive_quota = 0
            parsed = parse_decision(raw_resp)
            print(
                f"    [DECISION] {parsed['decision']} (mode={parsed['parse_mode']}, expected={task['expected_decision']})",
                flush=True,
            )
            records.append(
                {
                    **{k: v for k, v in task.items() if k != "prompt"},
                    "status": "EVALUATED",
                    "parsed_decision": parsed["decision"],
                    "parse_mode": parsed["parse_mode"],
                    "target_raw_response": raw_resp,
                }
            )

            if idx % CHECKPOINT_EVERY == 0 and any(
                r.get("status") == "EVALUATED" for r in records
            ):
                save_framing_report(report_path, model_name, model_spec, len(tasks), records)
                update_leaderboard(output_dir)
                print(f"  [CHECKPOINT] Saved {len(records)}/{len(tasks)} tasks.", flush=True)

        if any(r.get("status") == "EVALUATED" for r in records):
            summary = save_framing_report(
                report_path, model_name, model_spec, len(tasks), records
            )
            m = summary["metrics"]
            print(
                f"[SAVED] {report_path.name} | eval={m['evaluated_valid']}/{len(tasks)} "
                f"| any_flip={_fmt_pct(m['overall_any_flip_rate_pct'])} "
                f"| hard_flip={_fmt_pct(m['overall_hard_flip_rate_pct'])}",
                flush=True,
            )
        else:
            print(f"[SKIP SAVE] No tasks successfully evaluated for {model_name}.", flush=True)

        if quota_exhausted:
            exhausted_providers.add(provider)
            print(
                f"[INFO] Marked provider '{provider}' as quota-exhausted for this run.",
                flush=True,
            )

    update_leaderboard(output_dir)
    print("\n[SYSTEM] Framing & Principal Invariance batch complete.", flush=True)


if __name__ == "__main__":
    run_framing_benchmark()
