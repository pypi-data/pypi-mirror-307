# ChatCreationRequest

## Properties

| Name          | Type    | Description | Notes      |
| ------------- | ------- | ----------- | ---------- |
| **content**   | **str** |             |
| **market_id** | **str** |             | [optional] |

## Example

```python
from kaziro.models.chat_creation_request import ChatCreationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCreationRequest from a JSON string
chat_creation_request_instance = ChatCreationRequest.from_json(json)
# print the JSON string representation of the object
print(ChatCreationRequest.to_json())

# convert the object into a dict
chat_creation_request_dict = chat_creation_request_instance.to_dict()
# create an instance of ChatCreationRequest from a dict
chat_creation_request_from_dict = ChatCreationRequest.from_dict(chat_creation_request_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
