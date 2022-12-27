def get_secret_key() -> str:
    from os import environ

    secret_key = environ.get("MyIMGSecretKey", None)
    if not secret_key:
        from base64 import b64encode
        from secrets import token_bytes

        secret_key = b64encode(token_bytes(32)).decode()
    return secret_key


def get_config() -> dict:
    import json
    import os

    with open(os.path.join(os.path.dirname(__file__), "config.json")) as fp:
        json_object = json.load(fp)
        return json_object
