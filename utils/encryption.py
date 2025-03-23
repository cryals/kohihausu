def xor_encrypt_decrypt(data: bytes, key: str) -> bytes:
    """Шифрование/дешифрование с помощью XOR."""
    key_bytes = key.encode()
    return bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data))