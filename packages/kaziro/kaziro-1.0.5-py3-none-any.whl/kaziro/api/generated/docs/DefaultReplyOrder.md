# DefaultReplyOrder

## Properties

| Name            | Type                  | Description                                               | Notes      |
| --------------- | --------------------- | --------------------------------------------------------- | ---------- |
| **market_id**   | **str**               | Unique identifier for the market.                         |
| **status**      | **str**               | Status of the default reply operation (SUCCESS or ERROR). |
| **message**     | **str**               | Error message if status is ERROR.                         | [optional] |
| **reply_order** | [**Order**](Order.md) | Default reply order if status is SUCCESS.                 |
| **request_id**  | **str**               | Request ID associated with the order.                     |

## Example

```python
from kaziro.models.default_reply_order import DefaultReplyOrder

# TODO update the JSON string below
json = "{}"
# create an instance of DefaultReplyOrder from a JSON string
default_reply_order_instance = DefaultReplyOrder.from_json(json)
# print the JSON string representation of the object
print(DefaultReplyOrder.to_json())

# convert the object into a dict
default_reply_order_dict = default_reply_order_instance.to_dict()
# create an instance of DefaultReplyOrder from a dict
default_reply_order_from_dict = DefaultReplyOrder.from_dict(default_reply_order_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
