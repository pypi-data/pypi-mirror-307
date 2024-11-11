# WalletInfoResponse

## Properties

| Name        | Type                          | Description                                    | Notes |
| ----------- | ----------------------------- | ---------------------------------------------- | ----- |
| **success** | **bool**                      | Indicates if the operation was successful      |
| **message** | **str**                       | Descriptive message about the operation result |
| **wallets** | [**List[Wallet]**](Wallet.md) | Wallet information                             |

## Example

```python
from kaziro.models.wallet_info_response import WalletInfoResponse

# TODO update the JSON string below
json = "{}"
# create an instance of WalletInfoResponse from a JSON string
wallet_info_response_instance = WalletInfoResponse.from_json(json)
# print the JSON string representation of the object
print(WalletInfoResponse.to_json())

# convert the object into a dict
wallet_info_response_dict = wallet_info_response_instance.to_dict()
# create an instance of WalletInfoResponse from a dict
wallet_info_response_from_dict = WalletInfoResponse.from_dict(wallet_info_response_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
