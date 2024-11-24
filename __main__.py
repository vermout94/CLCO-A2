"""An Azure RM Python Pulumi program"""

import pulumi
from pulumi_azure_native import storage, resources

# Create an Azure Resource Group
resource_group = resources.ResourceGroup("resource_group")

# Retrieve configuration values
config = pulumi.Config("storage")
account_name = config.require("accountName")
sku = config.require("sku")
kind = config.require("kind")

# Create an Azure resource (Storage Account)
storage_account = storage.StorageAccount(
    account_name,
    resource_group_name=resource_group.name,
    sku=storage.SkuArgs(name=sku),
    kind=storage.Kind(kind),
    location=resource_group.location,
)

# Fetch the storage account's primary key
primary_key = pulumi.Output.all(resource_group.name, storage_account.name).apply(
    lambda args: storage.list_storage_account_keys_output(
        resource_group_name=args[0],
        account_name=args[1],
    ).apply(lambda account_keys: account_keys.keys[0].value)
)

# Export the primary key of the Storage Account
pulumi.export("primary_storage_key", primary_key)


#List all resource groups
#az group list --query "[].{Name:name}" -o table
