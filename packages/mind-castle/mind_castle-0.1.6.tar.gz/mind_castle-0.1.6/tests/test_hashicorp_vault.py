from unittest.mock import ANY

from mind_castle.stores.vault import HashiCorpVaultSecretStore


def test_put_secret(mocker):
    secret_store = HashiCorpVaultSecretStore()
    mocker.patch.object(
        secret_store.client.secrets.kv.v2, "create_or_update_secret", return_value={}
    )
    response = secret_store.put_secret("some_secret_value")

    assert secret_store.client.secrets.kv.v2.create_or_update_secret.called_once_with(
        secret=dict(path=ANY, secret_value="some_secret_value")
    )
    assert response.get("secret_type") == "hashicorpvault"
    assert response.get("key") is not None


def test_get_secret(mocker):
    mock_vault_response = {
        "data": {
            "data": {
                "secret_value": "some_secret_value",
            }
        }
    }

    secret_store = HashiCorpVaultSecretStore()
    mocker.patch.object(
        secret_store.client.secrets.kv,
        "read_secret_version",
        return_value=mock_vault_response,
    )
    response = secret_store.get_secret("some_secret_key2")

    assert secret_store.client.secrets.kv.read_secret_version.calle_once_with(
        path="some_secret_key2"
    )
    assert response == "some_secret_value"
