# ChatWithMarketAndOrder

## Properties

| Name             | Type                    | Description                                                                                                                                                                                                                                                    | Notes      |
| ---------------- | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| **id**           | **str**                 | Unique identifier for the chat message                                                                                                                                                                                                                         |
| **user_id**      | **str**                 | User identifier associated with the chat message                                                                                                                                                                                                               |
| **content**      | **str**                 | The content of the chat message                                                                                                                                                                                                                                |
| **date_created** | **str**                 | The date the message was created                                                                                                                                                                                                                               |
| **metadata**     | **object**              | Additional metadata for the chat message                                                                                                                                                                                                                       | [optional] |
| **market_id**    | **str**                 | Market identifier associated with the chat message                                                                                                                                                                                                             | [optional] |
| **order_id**     | **str**                 | Order identifier associated with the chat message                                                                                                                                                                                                              | [optional] |
| **is_global**    | **bool**                | Whether the chat message is global. A global chat message is visible to all users on Kaziro and is not associated with a particular market or order, while a non-global chat message is visible to the user who sent it and the creator of the market or order |
| **market**       | [**Market**](Market.md) |                                                                                                                                                                                                                                                                | [optional] |
| **order**        | [**Order**](Order.md)   |                                                                                                                                                                                                                                                                | [optional] |

## Example

```python
from kaziro.models.chat_with_market_and_order import ChatWithMarketAndOrder

# TODO update the JSON string below
json = "{}"
# create an instance of ChatWithMarketAndOrder from a JSON string
chat_with_market_and_order_instance = ChatWithMarketAndOrder.from_json(json)
# print the JSON string representation of the object
print(ChatWithMarketAndOrder.to_json())

# convert the object into a dict
chat_with_market_and_order_dict = chat_with_market_and_order_instance.to_dict()
# create an instance of ChatWithMarketAndOrder from a dict
chat_with_market_and_order_from_dict = ChatWithMarketAndOrder.from_dict(chat_with_market_and_order_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
