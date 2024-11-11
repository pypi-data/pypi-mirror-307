# ChatExtended

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
| **user**         | [**User**](User.md)     |                                                                                                                                                                                                                                                                | [optional] |

## Example

```python
from kaziro.models.chat_extended import ChatExtended

# TODO update the JSON string below
json = "{}"
# create an instance of ChatExtended from a JSON string
chat_extended_instance = ChatExtended.from_json(json)
# print the JSON string representation of the object
print(ChatExtended.to_json())

# convert the object into a dict
chat_extended_dict = chat_extended_instance.to_dict()
# create an instance of ChatExtended from a dict
chat_extended_from_dict = ChatExtended.from_dict(chat_extended_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
