# AcceptOrdersRequest

## Properties

| Name       | Type                                | Description                   | Notes |
| ---------- | ----------------------------------- | ----------------------------- | ----- |
| **orders** | [**List[OrderPair]**](OrderPair.md) | List of order pairs to accept |

## Example

```python
from kaziro.models.accept_orders_request import AcceptOrdersRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AcceptOrdersRequest from a JSON string
accept_orders_request_instance = AcceptOrdersRequest.from_json(json)
# print the JSON string representation of the object
print(AcceptOrdersRequest.to_json())

# convert the object into a dict
accept_orders_request_dict = accept_orders_request_instance.to_dict()
# create an instance of AcceptOrdersRequest from a dict
accept_orders_request_from_dict = AcceptOrdersRequest.from_dict(accept_orders_request_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
