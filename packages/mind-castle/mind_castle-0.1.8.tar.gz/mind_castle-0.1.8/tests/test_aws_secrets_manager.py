from moto import mock_aws

from mind_castle.stores.aws import AWSSecretsManagerSecretStore


@mock_aws
def test_put_secret(mocker):
    secret_store = AWSSecretsManagerSecretStore()
    response = secret_store.put_secret("some_secret_value")

    # Read the secret from AWS directly to check
    client = secret_store.client  # Use the same auth etc as the store
    boto_response = client.get_secret_value(SecretId=response["key"])
    assert boto_response["SecretString"] == "some_secret_value"


@mock_aws
def test_get_secret():
    secret_store = AWSSecretsManagerSecretStore()
    # Add secret directly to AWS
    client = secret_store.client  # Use the same auth etc as the store
    client.create_secret(Name="some_secret_key", SecretString="some_secret_value")

    assert secret_store.get_secret("some_secret_key") == "some_secret_value"
