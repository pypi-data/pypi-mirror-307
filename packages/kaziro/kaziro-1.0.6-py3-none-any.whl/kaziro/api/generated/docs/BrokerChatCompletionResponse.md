# BrokerChatCompletionResponse

## Properties

| Name        | Type                                                                  | Description | Notes                                     |
| ----------- | --------------------------------------------------------------------- | ----------- | ----------------------------------------- |
| **id**      | **str**                                                               |             |
| **object**  | **str**                                                               |             | [optional] [default to 'chat.completion'] |
| **created** | **int**                                                               |             |
| **model**   | **str**                                                               |             | [optional] [default to 'custom']          |
| **choices** | [**List[BrokerChatCompletionChoice]**](BrokerChatCompletionChoice.md) |             |
| **usage**   | **object**                                                            |             | [optional]                                |
| **extra**   | **object**                                                            |             | [optional]                                |

## Example

```python
from kaziro.models.broker_chat_completion_response import BrokerChatCompletionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BrokerChatCompletionResponse from a JSON string
broker_chat_completion_response_instance = BrokerChatCompletionResponse.from_json(json)
# print the JSON string representation of the object
print(BrokerChatCompletionResponse.to_json())

# convert the object into a dict
broker_chat_completion_response_dict = broker_chat_completion_response_instance.to_dict()
# create an instance of BrokerChatCompletionResponse from a dict
broker_chat_completion_response_from_dict = BrokerChatCompletionResponse.from_dict(broker_chat_completion_response_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
