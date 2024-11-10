def encode(content: str | bytes | bytearray, key: str | bytes | bytearray | int | float) -> bytes:
    if isinstance(content, str):
        content = content.encode()
    if isinstance(key, str):
        key = key.encode()
    elif isinstance(key, (int, float)):
        key = str(key).encode()

    encoded = bytearray()
    key_len = len(key)

    for i, byte in enumerate(content):
        encoded.append(byte ^ key[i % key_len])

    return bytes(encoded)


def decode(content: str | bytes | bytearray, key: str | bytes | bytearray | int | float) -> str:
    if isinstance(content, str):
        content = content.encode()
    if isinstance(key, str):
        key = key.encode()
    elif isinstance(key, (int, float)):
        key = str(key).encode()

    decoded = bytearray()
    key_len = len(key)

    for i, byte in enumerate(content):
        decoded.append(byte ^ key[i % key_len])

    return decoded.decode()
