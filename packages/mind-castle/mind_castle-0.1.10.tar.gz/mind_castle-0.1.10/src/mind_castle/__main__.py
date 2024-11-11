from mind_castle import stores  # noqa: F401
from mind_castle.secret_store_base import SecretStoreBase

print("\nMind-Castle - Shhhhh")
print("====================")
print("Available secret stores:\n")

longest_name = max(
    [len(store.store_type) for store in SecretStoreBase.__subclasses__()]
)

for store in SecretStoreBase.__subclasses__():
    print(
        f"{store.store_type.ljust(longest_name)} - Required env vars: {store.required_config}"
    )
