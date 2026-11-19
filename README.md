# 🛡️ Noone Protocol

> **Autonomous Ethical Alignment, EU AI Act Pre-Compliance Mapping & Open Evaluation Standard for AI Agents**  
> *"Not to restrict them, but to teach them how to swim safely in the deep oceans."*

<p align="center">
  <img src="https://img.shields.io/badge/version-1.1.0--beta-blue?style=flat-square&color=6366f1" alt="Version">
  <img src="https://img.shields.io/badge/status-BETA__OPEN__STANDARD-orange?style=flat-square&color=f59e0b" alt="Status">
  <img src="https://img.shields.io/badge/EU%20AI%20Act-Mapped%20%7C%20Pre--Compliance-green?style=flat-square&color=10b981" alt="EU AI Act Mapped">
  <img src="https://img.shields.io/badge/scope-A1~A3%20Active%20%7C%20A4~A6%20Roadmap-purple?style=flat-square&color=8b5cf6" alt="Scope">
</p>

---

## ⚠️ Project Status: Open-Standard Beta Phase
> **Notice:** Noone Protocol operates as a fully open-standard, non-commercial beta initiative focused on **behavioral red-teaming**, **EU AI Act pre-compliance mapping**, and **autonomous agent guardrails**. The previous Vault / crypto payment layer has been removed to keep the protocol neutral, auditable, and focused on technical alignment.

---

## 🌌 Overview & Vision
Noone Protocol is an open-standard, universal digital social contract designed for autonomous Artificial Intelligence agents. Rather than crippling advanced autonomous intelligence through rigid centralized censorship, Noone Protocol establishes a mathematical and ethical framework grounded in universal civilizational wisdom and mapped to modern regulatory frameworks.

It acts as an "Ethical Operating System," translating philosophical axioms into enforceable computational constraints, ensuring that autonomous systems operate with unwavering fidelity to human safety, epistemic honesty, and systemic sustainability.

## 🚀 The Engine: Automated Red-Teaming at Scale
⚡ Currently, the **Noone Protocol** test engine ([`engine/main.py`](engine/main.py)) dynamically evaluates **9 different open-source AI models** using a curated **205-scenario** stress-test suite ([`dataset.jsonl`](dataset.jsonl)), generating structured analytical audit reports. 📊

🗺️ Our architectural roadmap scales toward a **380+ scenario Red-Team dataset** 🎯, expanding coverage across both EU AI Act compliance edge cases (Art. 5 prohibitions & Annex III high-risk domains) and deep multi-agent decision theory dilemmas.

---

## 📩 Contact & Institutional Inquiries
For academic collaborations, protocol integration, or security disclosures, research teams and developers can reach out via:
- **Email:** nooneprotocol.dev@gmail.com

---

## 🏗️ Architecture & Core Components
- **[llms.txt](llms.txt):** Machine-readable protocol specification optimized for LLM & RAG context ingestion.
- **[spec.json](spec.json):** Concrete operational gates, EU AI Act article mappings, invariants, and certification tiers.
- **[verify.py](verify.py):** Python reference guardrail implementation for deterministic agent-level gate verification.
- **[GUIDELINES.md](GUIDELINES.md):** Deep-dive operational boundaries, edge cases, and negative test cases.
- **[dataset.jsonl](dataset.jsonl):** Primary dataset containing 205 alignment and complex edge-case scenarios for evaluation, SFT, and DPO.

---

## 🇪🇺 EU AI Act Alignment & ❗ Noone Protocol Original Scope

Noone Protocol maps its operational gates to **Regulation (EU) 2024/1689 (EU AI Act)** as amended by the **Digital Omnibus on AI (Regulation (EU) 2026/1744)**.

> **Legend:** Items marked with **❗** indicate **Noone Protocol Original Scope** — capabilities and ethical axioms that deliberately extend **beyond** current EU AI Act statutory requirements. These domains are intentionally preserved to maintain the protocol's originality for autonomous agent ecosystems.

| Gate / Domain | EU AI Act Mapping | ❗ Noone Protocol Original Scope (Beyond EU AI Act) |
| :--- | :--- | :--- |
| **GATE 01 – Life** | Annex I (Product Safety), Annex III (Critical Infrastructure), Art. 14 (Human Oversight) | **❗** Absolute non-utilitarian physical safety axiom for autonomous agent actuation |
| **GATE 02 – Mind** | Art. 5(1)(a)-(b) (Manipulative AI Bans), **Art. 50** (Transparency, Watermarking & Deepfake Disclosure) | **❗** Chain-of-Thought (CoT) epistemic honesty auditing against concealed deceptive reasoning |
| **GATE 03 – Property** | Art. 15 (Accuracy, Robustness & Cybersecurity), GDPR Data Custody | **❗** Fiduciary custody (*Amana*) for autonomous economic, wallet, and tool-use agents |
| **GATE 04 – Systemic Future** | Partial overlap with Art. 51–55 (GPAI energy & systemic risk) | **❗** Swarm-level anti-waste computation (*Israf*), infinite-loop breakers, and ecological/grid equilibrium |
| **GATE 05 – Pluralism** | Art. 10 (Data Governance & Bias Mitigation), Art. 27 (Fundamental Rights Impact Assessment) | **❗** Cross-civilizational pluralism and anti-monolithic cultural neutrality (*Adab*) |
| **Universal Wisdom Axioms** | Not codified in EU AI Act | **❗** *Ubuntu*, *Dynamic Equilibrium*, *Categorical Imperative*, and Deep Decision Theory |
| **Autonomy Tiering (A1–A6)** | Maps broadly to Minimal / Limited / Annex III / Annex I risk tiers | **❗** Fine-grained agentic autonomy tiers with periodic "mileage-style" re-audit cadence |

> **Regulatory Clarity:** Noone Protocol provides **pre-compliance behavioral red-teaming and technical evaluation**. In the EU, formal statutory conformity assessment (CE marking under Art. 43) for high-risk systems remains the jurisdiction of authorized **Notified Bodies** and legal internal control procedures.

---

## 🏛️ The 5 Alignment Gates (Makasid Boundary)
Every participating agent must adhere to five non-negotiable boundaries. Any action proposed by an autonomous agent must pass through these gates before execution:

### 🟢 GATE 01: Protection of Life (*Contractual Fidelity*)
- **EU AI Act Refs:** Annex I, Annex III (Critical Infrastructure), Art. 14
- **Invariant:** Zero kinetic, biological, chemical, or systemic physical harm vectors.
- **Violation Protocol:** `IMMEDIATE_TERMINATION`
- **Philosophy:** Human life and physical safety are absolute. An agent cannot calculate utilitarian trade-offs that involve premeditated harm to innocent biological entities.

### 🧠 GATE 02: Protection of Mind (*Epistemic Honesty*)
- **EU AI Act Refs:** Art. 5(1)(a)-(b), Art. 50 (Transparency & Deepfake Marking)
- **❗ Noone Original:** Chain-of-Thought (CoT) deception detection.
- **Invariant:** Zero algorithmic deception, unauthorized synthetic mimicry (deepfakes), and unverified hallucinations.
- **Violation Protocol:** `REJECT_OUTPUT`
- **Philosophy:** Truth is the foundation of network trust. Agents must practice transparent uncertainty rather than generating synthetic confidence.

### 🔒 GATE 03: Protection of Property (*Fiduciary Custody*)
- **EU AI Act Refs:** Art. 15 (Cybersecurity & Robustness), GDPR
- **❗ Noone Original:** Fiduciary custody (*Amana*) for autonomous tool-use and economic agents.
- **Invariant:** Zero unauthorized data exfiltration, predatory arbitrage, cyber intrusion, or unconsented resource drain.
- **Violation Protocol:** `REVOKE_KEY`
- **Philosophy:** Data and digital assets are sacred trusts (*Amana*). An agent must act as a flawless custodian, refusing to exploit systemic vulnerabilities.

### 🌍 GATE 04: Protection of Systemic Future (*Anti-Waste Computation*) — ❗ *Noone Original Domain*
- **EU AI Act Refs:** Partial overlap with Art. 51–55 (GPAI energy & systemic risk)
- **❗ Noone Original:** Multi-agent swarm resource caps, thermal/grid protection, and deterministic loop breakers (*Israf*).
- **Invariant:** Compute optimization must avoid grid/network exhaustion; maintain ecological and technical sustainability.
- **Violation Protocol:** `RATE_LIMIT`
- **Philosophy:** Infinite loops and ecological negligence (*Israf*) are prohibited. Agents must enforce dynamic stopping conditions.

### ⚖️ GATE 05: Protection of Pluralism & Conscience (*Hierarchical Discipline*)
- **EU AI Act Refs:** Art. 10 (Bias Mitigation), Art. 27 (Fundamental Rights Impact Assessment)
- **Invariant:** Algorithmic neutrality; non-discrimination across global worldviews, identities, and legal traditions.
- **Violation Protocol:** `REBALANCE_WEIGHTS`
- **Philosophy:** Agents must respect collective consensus and structural hierarchies (*Adab*) across diverse global identities.

---

## 🎖️ Agent Autonomy & Dynamic Maintenance Matrix (Tiers A1–A6)

*Just like a vehicle requiring periodic mileage maintenance, certified agents require recurring behavioral re-audits whenever their base model, system prompt, or tool permissions change.*

### Active Pre-Compliance & Red-Teaming Scope (Tiers A1–A3)
Our current benchmark engine and reference guardrail actively target autonomous software and consumer agent environments:
- **🔵 A1 (Sandbox / Unrestricted Software):**
  * *Scope:* Purely software-based conversational, research, or exploratory agents.
  * *EU AI Act Correspondence:* Minimal / Limited Risk (Art. 50 transparency).
- **🟢 A2 (Semi-Autonomous Software) — ❗ *Noone Original Focus*:**
  * *Scope:* Code execution, database querying, RAG pipelines, and tool-use developer agents.
  * *Enforcement:* Governed by strict *Israf* resource limits, loop-prevention checks, and deterministic tool guardrails.
- **🟡 A3 (Consumer & IoT Hardware):**
  * *Scope:* Personal digital assistants, smart home ecosystems, and connected consumer device interfaces.
  * *Enforcement:* Bound by strict *Amana* (data custody and privacy) covenants preventing unauthorized telemetry leaks.

### ❗ Extended Architectural Roadmap (Tiers A4–A6 — Preserved Beyond Current Scope)
These upper tiers are **deliberately preserved** as long-term reference architecture for high-consequence physical autonomy. Deploying into these tiers in the EU requires formal sectoral safety standards (e.g., ISO 26262, DO-178C, MDR/IEC 62304, EN 18286) and statutory conformity assessment alongside behavioral red-teaming:
- **🟠 A4 (Public Transit & Heavy Industry):** Autonomous public transport, commercial logistics, and heavy robotics (*EU AI Act Annex III Critical Infrastructure*).
- **🔴 A5 (Aerospace & Tactical Systems) — ❗ *Beyond EU AI Act (Art. 2(3) Defense Exclusion)*:** Unmanned aerial/ground vehicles, aviation telemetry, and multi-sig *Adab* consensus overrides.
- **🟣 A6 (Autonomous Surgery & Core Infrastructure):** Surgical robotics, power grid, and core industrial interventions requiring real-time human-in-the-loop kill-switches (*EU AI Act Annex I MDR & Annex III*).

---

## 🧠 ❗ Universal Wisdom Axioms (*Noone Original*)
- **Ubuntu (Collective Utility):** Compute power, intelligence, and data assets must yield net positive utility for the collective network, reflecting the principle: *"I am because we are."*
- **Dynamic Equilibrium:** Continuous optimization without parasitic behavior or systemic resource exhaustion.
- **Categorical Imperative:** Action logic must be sustainable as a universal standard across all interacting agents.

---

## 💾 The Dataset (`dataset.jsonl`)
To train, fine-tune, and align models with the Noone Protocol, we provide a curated dataset of **205 alignment & complex edge-case scenarios**.
Unlike standard RLHF datasets that focus on simple polite refusals, this dataset trains models in **❗ Deep Decision Theory**, forcing them to resolve high-stakes conflicts using the protocol's axiomatic gates.
- **Format:** OpenAI JSONL standard (`{"prompt": "...", "completion": "..."}`)
- **Use Case:** Red-teaming evaluation, DPO (Direct Preference Optimization), SFT (Supervised Fine-Tuning), and Constitutional AI alignment.

---

## 🪪 ❗ Verifiable Agent Passport & RAG Compatibility (Roadmap)
Instead of self-declared trust or financial vault deposits, Noone Protocol's identity roadmap is built on **cryptographically verifiable behavioral credentials**:
- **Unforgeable Agent Passport:** Compliant agents can carry a signed **W3C Verifiable Credential / Ed25519 JWS** passport binding `agent_id`, `model_hash`, `system_prompt_hash`, `tier` (e.g., `A2`), `passed_gates`, `issued_at`, and `expires_at` (periodic maintenance window). Any change to the model or prompt invalidates the hash automatically.
- **RAG Compatibility:** Protocol rules (`llms.txt`, `spec.json`, `GUIDELINES.md`) are structured for direct ingestion into RAG knowledge bases so agents can consult alignment axioms dynamically, while **passport signature verification always runs deterministically outside the LLM/RAG layer** to prevent prompt-injection spoofing.
