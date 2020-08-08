import hashlib


def encrypt_with_sha_256(text):
    return hashlib.sha256(text.encode()).hexdigest()