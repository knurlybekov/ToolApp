from toolapp_security import hash_password, verify_password, is_hashed


def test_hash_roundtrip():
    h = hash_password("correct horse")
    assert is_hashed(h)
    assert verify_password(h, "correct horse") == (True, False)
    assert verify_password(h, "wrong") == (False, False)


def test_legacy_plaintext_is_accepted_once_and_flagged():
    assert verify_password("plain", "plain") == (True, True)
    assert verify_password("plain", "nope") == (False, False)


def test_empty_values_fail():
    assert verify_password("", "x") == (False, False)
    assert verify_password(None, "x") == (False, False)
