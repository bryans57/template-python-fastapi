import base64


def decode_base64_password(encoded_password):
    decoded_bytes = base64.b64decode(encoded_password)
    return decoded_bytes.decode("utf-8")
