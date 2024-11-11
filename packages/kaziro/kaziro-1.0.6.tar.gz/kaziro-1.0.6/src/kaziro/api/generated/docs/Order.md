# Order

## Properties

| Name             | Type       | Description                                   | Notes      |
| ---------------- | ---------- | --------------------------------------------- | ---------- |
| **id**           | **str**    | Unique identifier for the created order.      |
| **date_created** | **str**    | Timestamp of order creation.                  |
| **market_id**    | **str**    | Market identifier for the order.              |
| **wallet_id**    | **str**    | Wallet identifier associated with the order.  | [optional] |
| **status**       | **str**    | Current status of the order.                  |
| **probability**  | **float**  | Probability set for the order.                | [optional] |
| **size**         | **float**  | Size of the order.                            |
| **order_type**   | **str**    | Type of the order.                            |
| **expiry_type**  | **str**    | Expiration type of the order.                 |
| **request_id**   | **str**    | Request identifier associated with the order. | [optional] |
| **metadata**     | **object** | Metadata associated with the order.           | [optional] |

## Example

```python
from kaziro.models.order import Order

# TODO update the JSON string below
json = "{}"
# create an instance of Order from a JSON string
order_instance = Order.from_json(json)
# print the JSON string representation of the object
print(Order.to_json())

# convert the object into a dict
order_dict = order_instance.to_dict()
# create an instance of Order from a dict
order_from_dict = Order.from_dict(order_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
