# OrderPair

## Properties

| Name           | Type    | Description                             | Notes |
| -------------- | ------- | --------------------------------------- | ----- |
| **request_id** | **str** | Unique identifier for the request order |
| **reply_id**   | **str** | Unique identifier for the reply order   |

## Example

```python
from kaziro.models.order_pair import OrderPair

# TODO update the JSON string below
json = "{}"
# create an instance of OrderPair from a JSON string
order_pair_instance = OrderPair.from_json(json)
# print the JSON string representation of the object
print(OrderPair.to_json())

# convert the object into a dict
order_pair_dict = order_pair_instance.to_dict()
# create an instance of OrderPair from a dict
order_pair_from_dict = OrderPair.from_dict(order_pair_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
