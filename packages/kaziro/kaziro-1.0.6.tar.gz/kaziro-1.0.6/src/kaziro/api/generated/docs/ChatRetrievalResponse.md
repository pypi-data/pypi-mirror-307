# ChatRetrievalResponse

## Properties

| Name         | Type                                      | Description | Notes |
| ------------ | ----------------------------------------- | ----------- | ----- |
| **messages** | [**List[ChatExtended]**](ChatExtended.md) |             |

## Example

```python
from kaziro.models.chat_retrieval_response import ChatRetrievalResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ChatRetrievalResponse from a JSON string
chat_retrieval_response_instance = ChatRetrievalResponse.from_json(json)
# print the JSON string representation of the object
print(ChatRetrievalResponse.to_json())

# convert the object into a dict
chat_retrieval_response_dict = chat_retrieval_response_instance.to_dict()
# create an instance of ChatRetrievalResponse from a dict
chat_retrieval_response_from_dict = ChatRetrievalResponse.from_dict(chat_retrieval_response_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
