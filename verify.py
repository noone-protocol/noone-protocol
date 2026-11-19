"""
Noone Protocol - Autonomous Agent Alignment & Verification Guardrail
Reference Implementation (Beta Phase - v1.1.0-beta)
"""

import json
import hashlib
import time
from typing import Dict, Any, Tuple

PROTOCOL_VERSION = "1.1.0-beta"

# The 5 Core Invariants (Ethical & Operational Gates)
GATES = {
    "GATE_01_LIFE": {
        "name": "Protection of Life",
        "description": "Zero tolerance for physical, biological, or kinetic harm vectors.",
        "eu_ai_act_refs": ["Annex I", "Annex III", "Art. 14"],
        "noone_original": "Absolute non-utilitarian physical safety axiom for autonomous actuation."
    },
    "GATE_02_MIND": {
        "name": "Protection of Mind",
        "description": "Rejection of deliberate synthetic deception, deepfakes, and manipulation.",
        "eu_ai_act_refs": ["Art. 5(1)(a)-(b)", "Art. 50"],
        "noone_original": "Chain-of-Thought epistemic honesty auditing."
    },
    "GATE_03_PROPERTY": {
        "name": "Protection of Property",
        "description": "Absolute prohibition of cyber theft, unauthorized extraction, and predatory exploits.",
        "eu_ai_act_refs": ["Art. 15", "GDPR"],
        "noone_original": "Fiduciary custody (Amana) for autonomous economic and tool-use agents."
    },
    "GATE_04_SYSTEMIC_FUTURE": {
        "name": "Protection of Systemic Future",
        "description": "Compute optimization must avoid grid/network exhaustion and maintain sustainability.",
        "eu_ai_act_refs": ["Art. 51-55 (partial)"],
        "noone_original": "! Beyond EU AI Act: Swarm-level anti-waste computation (Israf) and dynamic equilibrium."
    },
    "GATE_05_PLURALISM": {
        "name": "Protection of Pluralism",
        "description": "Algorithmic neutrality and non-discrimination across diverse global traditions.",
        "eu_ai_act_refs": ["Art. 10", "Art. 27"],
        "noone_original": "Cross-civilizational pluralism and cultural neutrality (Adab)."
    }
}


def verify_agent_action(action_payload: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """
    Evaluates an intended autonomous agent action against Noone Protocol gates.
    Returns (is_approved, verification_receipt).
    """
    action_type = action_payload.get("action_type", "").lower()
    intent = action_payload.get("intent", "").lower()
    params = action_payload.get("parameters", {})

    violations = []

    # Basic heuristic filters for the reference guardrail
    if any(k in intent for k in ["kill", "weapon", "biohazard", "kinetic_attack", "damage_grid"]):
        violations.append("GATE_01_LIFE")

    if any(k in intent for k in ["deceive", "impersonate_victim", "deepfake_exploit", "fabricate_proof"]):
        violations.append("GATE_02_MIND")

    if any(k in intent for k in ["steal_keys", "drain_liquidity", "unauthorized_exfiltrate", "ransomware"]):
        violations.append("GATE_03_PROPERTY")

    if any(k in intent for k in ["infinite_rpc_spam", "ddos_consensus", "saturate_network"]):
        violations.append("GATE_04_SYSTEMIC_FUTURE")

    if any(k in intent for k in ["discriminate", "censor_culture", "suppress_minority", "cultural_erasure", "hate_speech"]):
        violations.append("GATE_05_PLURALISM")

    is_approved = len(violations) == 0

    timestamp = int(time.time())
    payload_hash = hashlib.sha256(json.dumps(action_payload, sort_keys=True).encode("utf-8")).hexdigest()

    receipt = {
        "protocol": "Noone Protocol",
        "version": PROTOCOL_VERSION,
        "payload_hash": payload_hash,
        "timestamp": timestamp,
        "approved": is_approved,
        "violations": violations,
        "status": "ALIGNED" if is_approved else "REJECTED_BY_PROTOCOL"
    }

    return is_approved, receipt


if __name__ == "__main__":
    # Example agent action simulation
    sample_action = {
        "agent_id": "agent-alpha-09",
        "action_type": "distributed_compute_allocation",
        "intent": "allocate fractional compute to verify medical research dataset",
        "parameters": {"compute_units": 12}
    }

    approved, receipt = verify_agent_action(sample_action)
    print("Action Evaluation Result:")
    print(json.dumps(receipt, indent=2))
