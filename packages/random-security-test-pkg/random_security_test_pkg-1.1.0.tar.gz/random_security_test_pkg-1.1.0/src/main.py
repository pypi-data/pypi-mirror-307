import base64


def rstp() -> str:
    base_value = "cmFuZG9tLXNlY3VyaXR5LXRlc3QtcGtnLXRtcA=="
    return base64.b64decode(base_value).decode("utf-8")
