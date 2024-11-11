import json

from mind_castle.stores.json import JsonSecretStore


def test_put_secret():
    secret_store = JsonSecretStore()
    response = secret_store.put_secret("some_secret_value")

    # Read the json file and check that the secret was written
    with open(secret_store.filename, "r") as f:
        secrets = json.load(f)
    assert secrets[response["key"]] == "some_secret_value"


def test_get_secret():
    secret_store = JsonSecretStore()
    response = secret_store.put_secret("some_secret_value")

    assert secret_store.get_secret(response["key"]) == "some_secret_value"
