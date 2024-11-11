# OpenOrdersResponse

## Properties

| Name        | Type                                        | Description                                     | Notes |
| ----------- | ------------------------------------------- | ----------------------------------------------- | ----- |
| **success** | **bool**                                    | Indicates if the operation was successful.      |
| **message** | **str**                                     | Descriptive message about the operation result. |
| **orders**  | [**List[OrderExtended]**](OrderExtended.md) | List of open orders.                            |

## Example

```python
from kaziro.models.open_orders_response import OpenOrdersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of OpenOrdersResponse from a JSON string
open_orders_response_instance = OpenOrdersResponse.from_json(json)
# print the JSON string representation of the object
print(OpenOrdersResponse.to_json())

# convert the object into a dict
open_orders_response_dict = open_orders_response_instance.to_dict()
# create an instance of OpenOrdersResponse from a dict
open_orders_response_from_dict = OpenOrdersResponse.from_dict(open_orders_response_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
