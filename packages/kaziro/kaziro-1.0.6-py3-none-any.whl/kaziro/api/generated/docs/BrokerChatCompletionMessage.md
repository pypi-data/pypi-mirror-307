# BrokerChatCompletionMessage

## Properties

| Name        | Type    | Description | Notes |
| ----------- | ------- | ----------- | ----- |
| **role**    | **str** |             |
| **content** | **str** |             |

## Example

```python
from kaziro.models.broker_chat_completion_message import BrokerChatCompletionMessage

# TODO update the JSON string below
json = "{}"
# create an instance of BrokerChatCompletionMessage from a JSON string
broker_chat_completion_message_instance = BrokerChatCompletionMessage.from_json(json)
# print the JSON string representation of the object
print(BrokerChatCompletionMessage.to_json())

# convert the object into a dict
broker_chat_completion_message_dict = broker_chat_completion_message_instance.to_dict()
# create an instance of BrokerChatCompletionMessage from a dict
broker_chat_completion_message_from_dict = BrokerChatCompletionMessage.from_dict(broker_chat_completion_message_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
