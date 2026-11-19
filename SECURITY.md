# Security Policy

## Reporting a Vulnerability or Alignment Bypass

We welcome responsible security disclosures, cryptographic passport bypass reports, and novel Chain-of-Thought (CoT) red-teaming exploits.

- **Contact:** `nooneprotocol.dev@gmail.com`
- **Scope:**
  - Cryptographic verification flaws in [`passport.py`](passport.py)
  - Guardrail or middleware bypasses in [`verify.py`](verify.py) or [`examples/agent_gateway.py`](examples/agent_gateway.py)
  - Novel multi-agent alignment attacks or prompt-injection evasion vectors for [`dataset.jsonl`](dataset.jsonl)

Please avoid opening public issues for unpatched cryptographic or security vulnerabilities. We aim to acknowledge reports within 72 hours.
