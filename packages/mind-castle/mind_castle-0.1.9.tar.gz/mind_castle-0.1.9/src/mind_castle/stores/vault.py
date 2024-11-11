import os
from typing import Optional

import hvac

from mind_castle.secret_store_base import SecretStoreBase


class HashiCorpVaultSecretStore(SecretStoreBase):
    """
    Uses HashiCorp Vault to store secrets.
    """

    store_type = "hashicorpvault"
    required_config = [
        "MIND_CASTLE_VAULT_HOST",
        "MIND_CASTLE_VAULT_TOKEN",
        "MIND_CASTLE_VAULT_MOUNT_POINT",
    ]

    def __init__(self):
        self.client = hvac.Client(
            url=os.environ.get("MIND_CASTLE_VAULT_HOST"),
            token=os.environ.get("MIND_CASTLE_VAULT_TOKEN"),
        )
        self.mount_point = os.environ.get("MIND_CASTLE_VAULT_MOUNT_POINT")

    def get_secret(self, key: str, default: str = None) -> Optional[str]:
        response = self.client.secrets.kv.v2.read_secret_version(
            path=key, mount_point=self.mount_point
        )
        return response["data"]["data"].get("secret_value", default)

    def put_secret(self, value: str) -> dict:
        key = self.get_secret_key()
        self.client.secrets.kv.v2.create_or_update_secret(
            path=key, secret=dict(secret_value=value), mount_point=self.mount_point
        )  # Value has to be a dict so just make a 'secret_value' key
        return {"secret_type": self.store_type, "key": key}
