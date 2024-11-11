# AcceptedOrder

## Properties

| Name           | Type                        | Description                                   | Notes |
| -------------- | --------------------------- | --------------------------------------------- | ----- |
| **request_id** | **str**                     | Request identifier associated with the order. |
| **reply_id**   | **str**                     | Reply identifier associated with the order.   |
| **status**     | **str**                     | Status of the acceptance operation.           |
| **position**   | [**Position**](Position.md) | Position created for the accepted order.      |

## Example

```python
from kaziro.models.accepted_order import AcceptedOrder

# TODO update the JSON string below
json = "{}"
# create an instance of AcceptedOrder from a JSON string
accepted_order_instance = AcceptedOrder.from_json(json)
# print the JSON string representation of the object
print(AcceptedOrder.to_json())

# convert the object into a dict
accepted_order_dict = accepted_order_instance.to_dict()
# create an instance of AcceptedOrder from a dict
accepted_order_from_dict = AcceptedOrder.from_dict(accepted_order_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
