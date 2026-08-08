"""Cryptographic SHA-256 SEBI Provenance Stamping."""
import hashlib
import json
from typing import Dict, Any


def generate_sebi_audit_hash(payload: Dict[str, Any]) -> str:
    """Generate a deterministic 64-character SHA-256 cryptographic provenance hash.
    
    Ensures that identical input vectors and calculated diagnostic outputs
    produce bit-for-bit identical audit hashes for regulatory compliance.
    """
    # Canonical JSON string serialization (sorted keys, compact separators)
    canonical_json = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    hash_object = hashlib.sha256(canonical_json.encode("utf-8"))
    return hash_object.hexdigest()


def verify_sebi_audit_hash(payload: Dict[str, Any], claimed_hash: str) -> bool:
    """Verify if a claimed audit hash matches the recomputed hash from the payload."""
    recomputed = generate_sebi_audit_hash(payload)
    return recomputed.lower() == claimed_hash.lower()
