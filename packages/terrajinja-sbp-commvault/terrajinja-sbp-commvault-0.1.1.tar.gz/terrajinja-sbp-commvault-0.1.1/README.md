# terrajinja-sbp-commvault

This is an extension to the vault provider for the following modules.
The original documentation can be found [here](https://registry.terraform.io/providers/Commvault/commvault/latest/docs)

# SBP Specific implementations
Here is a list of supported resources and their modifications

## sbp.commvault.data_commvault_client
Original provider: [commvault.data_commvault_client](https://registry.terraform.io/providers/Commvault/commvault/latest/docs/data-sources/commvault_client)

### terrajinja-cli example
the following is a code snipet you can used in a terrajinja-cli template file.
This custom provider adds the following: it's converts the retrieved string to a number.

```
terraform:
  resources:
    - task: read-client_name
      module: sbp.commvault.data_commvault_client
      parameters:
          name: <client_name>
```


