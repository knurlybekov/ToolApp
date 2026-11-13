"""Password handling for the employees table.

Stored values are werkzeug PBKDF2/scrypt hashes. Rows seeded before hashing was introduced may still hold
plaintext; verify_password accepts them once so the login path can re-hash and store the hash (see auth.py).
"""
from werkzeug.security import check_password_hash, generate_password_hash

HASH_PREFIXES = ('pbkdf2:', 'scrypt:')


def is_hashed(stored: str) -> bool:
    return isinstance(stored, str) and stored.startswith(HASH_PREFIXES)


def hash_password(plain: str) -> str:
    return generate_password_hash(plain)


def verify_password(stored: str, candidate: str) -> tuple[bool, bool]:
    """Return (ok, needs_rehash). Legacy plaintext rows match by equality and are flagged for re-hashing."""
    if not stored or candidate is None:
        return False, False
    if is_hashed(stored):
        return check_password_hash(stored, candidate), False
    return (stored == candidate), (stored == candidate)
