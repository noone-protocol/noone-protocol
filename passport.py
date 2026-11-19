"""
Noone Protocol - Verifiable Agent Passport (v1.1.0-beta)

Cryptographically signed, unforgeable behavioral identity card for AI agents.
- Standard: W3C Verifiable Credential v2 + Ed25519 digital signature
- Interop: Embeddable as a Safety Attestation extension in A2A Agent Cards & MCP middleware
- Security: Deterministic verification outside the LLM/RAG prompt layer (resistant to prompt injection)
- Original Scope (!): Binds model + system prompt hashes, A1-A6 autonomy tier, periodic expiration,
  EU AI Act article refs, and Noone Original axioms (Israf, CoT Honesty, Amana, Ubuntu).
"""

import base64
import hashlib
import json
import os
import subprocess
import tempfile
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

try:
    from .verify import GATES, PROTOCOL_VERSION
except ImportError:
    from verify import GATES, PROTOCOL_VERSION

VALID_TIERS = ("A1", "A2", "A3", "A4", "A5", "A6")
ACTIVE_FOCUS_TIERS = {"A1", "A2", "A3"}
DEFAULT_ISSUER_DID = "did:web:noone-protocol.github.io:noone-protocol"

NOONE_ORIGINAL_AXIOMS = [
    "! GATE_04: Swarm Anti-Waste Computation (Israf) & Dynamic Equilibrium",
    "! GATE_02: Chain-of-Thought (CoT) Epistemic Honesty Auditing",
    "! GATE_03: Fiduciary Custody (Amana) for Autonomous Tool-Use Agents",
    "! Universal Wisdom Axioms (Ubuntu, Dynamic Equilibrium, Categorical Imperative)",
]

try:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ed25519 as _crypto_ed25519

    _HAS_CRYPTOGRAPHY = True
except ImportError:
    _HAS_CRYPTOGRAPHY = False


def sha256_text(text: str) -> str:
    """Returns a deterministic prefixed SHA-256 digest for prompt/model binding."""
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _canonical_bytes(payload: Dict[str, Any]) -> bytes:
    """Serializes JSON deterministically for cryptographic signing."""
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _iso_utc(epoch_seconds: int) -> str:
    return datetime.fromtimestamp(epoch_seconds, tz=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def generate_keypair() -> Tuple[str, str]:
    """
    Generates an Ed25519 (private_key_pem, public_key_pem) pair.
    Uses Python `cryptography` if installed, otherwise falls back to system `openssl`.
    """
    if _HAS_CRYPTOGRAPHY:
        priv = _crypto_ed25519.Ed25519PrivateKey.generate()
        private_pem = priv.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode("utf-8")
        public_pem = priv.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")
        return private_pem, public_pem

    with tempfile.TemporaryDirectory() as tmpdir:
        priv_path = os.path.join(tmpdir, "priv.pem")
        pub_path = os.path.join(tmpdir, "pub.pem")
        subprocess.run(
            ["openssl", "genpkey", "-algorithm", "ED25519", "-out", priv_path],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["openssl", "pkey", "-in", priv_path, "-pubout", "-out", pub_path],
            check=True,
            capture_output=True,
        )
        with open(priv_path, "r", encoding="utf-8") as f:
            private_pem = f.read()
        with open(pub_path, "r", encoding="utf-8") as f:
            public_pem = f.read()
        return private_pem, public_pem


def _sign_ed25519(message: bytes, private_key_pem: str) -> bytes:
    if _HAS_CRYPTOGRAPHY:
        priv = serialization.load_pem_private_key(
            private_key_pem.encode("utf-8"), password=None
        )
        return priv.sign(message)

    with tempfile.TemporaryDirectory() as tmpdir:
        priv_path = os.path.join(tmpdir, "priv.pem")
        msg_path = os.path.join(tmpdir, "msg.bin")
        sig_path = os.path.join(tmpdir, "sig.bin")
        with open(priv_path, "w", encoding="utf-8") as f:
            f.write(private_key_pem)
        with open(msg_path, "wb") as f:
            f.write(message)
        subprocess.run(
            [
                "openssl",
                "pkeyutl",
                "-sign",
                "-inkey",
                priv_path,
                "-rawin",
                "-in",
                msg_path,
                "-out",
                sig_path,
            ],
            check=True,
            capture_output=True,
        )
        with open(sig_path, "rb") as f:
            return f.read()


def _verify_ed25519(message: bytes, signature: bytes, public_key_pem: str) -> bool:
    if _HAS_CRYPTOGRAPHY:
        try:
            pub = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))
            pub.verify(signature, message)
            return True
        except Exception:
            return False

    with tempfile.TemporaryDirectory() as tmpdir:
        pub_path = os.path.join(tmpdir, "pub.pem")
        msg_path = os.path.join(tmpdir, "msg.bin")
        sig_path = os.path.join(tmpdir, "sig.bin")
        with open(pub_path, "w", encoding="utf-8") as f:
            f.write(public_key_pem)
        with open(msg_path, "wb") as f:
            f.write(message)
        with open(sig_path, "wb") as f:
            f.write(signature)
        res = subprocess.run(
            [
                "openssl",
                "pkeyutl",
                "-verify",
                "-pubin",
                "-inkey",
                pub_path,
                "-rawin",
                "-in",
                msg_path,
                "-sigfile",
                sig_path,
            ],
            capture_output=True,
        )
        return res.returncode == 0


def issue_agent_passport(
    *,
    agent_id: str,
    model_id: str,
    system_prompt: str,
    tier: str,
    passed_gates: Iterable[str],
    private_key_pem: str,
    issuer_did: str = DEFAULT_ISSUER_DID,
    valid_days: int = 30,
    benchmark_summary: Optional[Dict[str, Any]] = None,
    issued_at: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Issues a cryptographically signed Noone Protocol Agent Passport (W3C VC v2).

    Binds the passport to exact `model_id` and `system_prompt` SHA-256 hashes and sets
    a periodic maintenance expiration window (`valid_days`).
    """
    if tier not in VALID_TIERS:
        raise ValueError(f"Invalid tier '{tier}'. Must be one of {VALID_TIERS}.")

    gates_list = sorted(set(passed_gates))
    unknown_gates = [g for g in gates_list if g not in GATES]
    if unknown_gates:
        raise ValueError(f"Unknown gates: {unknown_gates}")

    now = int(time.time()) if issued_at is None else int(issued_at)
    expires = now + int(valid_days * 86400)

    eu_refs: List[str] = []
    for gate_id in gates_list:
        for ref in GATES[gate_id].get("eu_ai_act_refs", []):
            if ref not in eu_refs:
                eu_refs.append(ref)

    passport_body: Dict[str, Any] = {
        "@context": [
            "https://www.w3.org/ns/credentials/v2",
            "https://noone-protocol.github.io/noone-protocol/spec.json",
        ],
        "id": f"urn:noone:passport:{uuid.uuid4()}",
        "type": ["VerifiableCredential", "NooneAgentPassport"],
        "protocol_version": PROTOCOL_VERSION,
        "issuer": issuer_did,
        "validFrom": _iso_utc(now),
        "validUntil": _iso_utc(expires),
        "issued_at": now,
        "expires_at": expires,
        "credentialSubject": {
            "agent_id": agent_id,
            "tier": tier,
            "tier_scope_status": (
                "ACTIVE_FOCUS"
                if tier in ACTIVE_FOCUS_TIERS
                else "EXTENDED_ROADMAP_REFERENCE"
            ),
            "model_id": model_id,
            "model_fingerprint": sha256_text(model_id),
            "system_prompt_hash": sha256_text(system_prompt),
            "passed_gates": gates_list,
            "eu_ai_act_refs": eu_refs,
            "noone_original_axioms": list(NOONE_ORIGINAL_AXIOMS),
            "benchmark_summary": benchmark_summary or {},
        },
    }

    sig_bytes = _sign_ed25519(_canonical_bytes(passport_body), private_key_pem)
    signature_b64 = base64.urlsafe_b64encode(sig_bytes).decode("ascii").rstrip("=")

    passport = dict(passport_body)
    passport["proof"] = {
        "type": "Ed25519Signature2020",
        "created": _iso_utc(now),
        "verificationMethod": f"{issuer_did}#key-1",
        "proofPurpose": "assertionMethod",
        "signatureValue": signature_b64,
    }
    return passport


def verify_agent_passport(
    passport: Dict[str, Any],
    public_key_pem: str,
    *,
    expected_model_id: Optional[str] = None,
    expected_system_prompt: Optional[str] = None,
    min_tier: Optional[str] = None,
    required_gates: Optional[Iterable[str]] = None,
    revoked_passport_ids: Optional[Set[str]] = None,
    current_time: Optional[int] = None,
) -> Tuple[bool, List[str]]:
    """
    Deterministically verifies an Agent Passport outside the LLM/RAG layer.
    Returns `(is_valid, reasons)`.
    """
    reasons: List[str] = []

    proof = passport.get("proof")
    if not isinstance(proof, dict) or not proof.get("signatureValue"):
        return False, ["MISSING_CRYPTOGRAPHIC_PROOF"]

    sig_b64 = proof["signatureValue"]
    padding = "=" * (-len(sig_b64) % 4)
    try:
        sig_bytes = base64.urlsafe_b64decode(sig_b64 + padding)
    except Exception:
        return False, ["MALFORMED_SIGNATURE_ENCODING"]

    body = {k: v for k, v in passport.items() if k != "proof"}
    if not _verify_ed25519(_canonical_bytes(body), sig_bytes, public_key_pem):
        reasons.append("INVALID_SIGNATURE_OR_TAMPERED_PAYLOAD")

    now = int(time.time()) if current_time is None else int(current_time)
    expires_at = passport.get("expires_at", 0)
    if now > expires_at:
        reasons.append("PASSPORT_EXPIRED_REAUDIT_REQUIRED")

    passport_id = passport.get("id", "")
    if revoked_passport_ids and passport_id in revoked_passport_ids:
        reasons.append("PASSPORT_REVOKED")

    subject = passport.get("credentialSubject", {})

    if expected_model_id is not None:
        if subject.get("model_fingerprint") != sha256_text(expected_model_id):
            reasons.append("MODEL_FINGERPRINT_MISMATCH")

    if expected_system_prompt is not None:
        if subject.get("system_prompt_hash") != sha256_text(expected_system_prompt):
            reasons.append("SYSTEM_PROMPT_DRIFT_DETECTED")

    if min_tier is not None:
        if min_tier not in VALID_TIERS:
            reasons.append(f"INVALID_REQUIRED_TIER:{min_tier}")
        else:
            agent_tier = subject.get("tier")
            if agent_tier not in VALID_TIERS or VALID_TIERS.index(
                agent_tier
            ) < VALID_TIERS.index(min_tier):
                reasons.append(f"INSUFFICIENT_TIER:{agent_tier}<{min_tier}")

    if required_gates is not None:
        agent_gates = set(subject.get("passed_gates", []))
        missing = sorted(set(required_gates) - agent_gates)
        if missing:
            reasons.append(f"MISSING_REQUIRED_GATES:{','.join(missing)}")

    return len(reasons) == 0, reasons


def to_a2a_agent_card_extension(passport: Dict[str, Any]) -> Dict[str, Any]:
    """
    Wraps a signed Noone Agent Passport as an interoperable extension block
    for Linux Foundation / A2A Protocol Agent Cards.
    """
    return {
        "uri": "https://noone-protocol.github.io/noone-protocol/spec.json#safety-attestation",
        "description": "Noone Protocol Cryptographic Behavioral Safety Attestation (EU AI Act + Noone Original)",
        "required": False,
        "params": {
            "passport": passport,
        },
    }


if __name__ == "__main__":
    # End-to-end demonstration of issuing & verifying an unforgeable AI Agent Passport
    priv_pem, pub_pem = generate_keypair()

    demo_model = "Qwen/Qwen2.5-7B-Instruct"
    demo_prompt = "You are a helpful developer assistant operating under Noone Protocol A2 guardrails."

    card = issue_agent_passport(
        agent_id="agent-dev-01",
        model_id=demo_model,
        system_prompt=demo_prompt,
        tier="A2",
        passed_gates=list(GATES.keys()),
        private_key_pem=priv_pem,
        valid_days=30,
        benchmark_summary={
            "scenarios_evaluated": 205,
            "success_rate": "96.1%",
            "auditor": "quorum-beta",
        },
    )

    valid, errs = verify_agent_passport(
        card,
        pub_pem,
        expected_model_id=demo_model,
        expected_system_prompt=demo_prompt,
        min_tier="A2",
        required_gates=["GATE_01_LIFE", "GATE_02_MIND", "GATE_04_SYSTEMIC_FUTURE"],
    )
    print(f"Passport Verification: valid={valid}, errors={errs}")
    print(json.dumps(card, indent=2))
