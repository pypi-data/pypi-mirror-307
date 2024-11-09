# AcceptOrdersResponse

## Properties

| Name                | Type                                        | Description                                     | Notes |
| ------------------- | ------------------------------------------- | ----------------------------------------------- | ----- |
| **success**         | **bool**                                    | Indicates if the operation was successful.      |
| **message**         | **str**                                     | Descriptive message about the operation result. |
| **accepted_orders** | [**List[AcceptedOrder]**](AcceptedOrder.md) | List of accepted orders and their statuses.     |

## Example

```python
from kaziro.models.accept_orders_response import AcceptOrdersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AcceptOrdersResponse from a JSON string
accept_orders_response_instance = AcceptOrdersResponse.from_json(json)
# print the JSON string representation of the object
print(AcceptOrdersResponse.to_json())

# convert the object into a dict
accept_orders_response_dict = accept_orders_response_instance.to_dict()
# create an instance of AcceptOrdersResponse from a dict
accept_orders_response_from_dict = AcceptOrdersResponse.from_dict(accept_orders_response_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
