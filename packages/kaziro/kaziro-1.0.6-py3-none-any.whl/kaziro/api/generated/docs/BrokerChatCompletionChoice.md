# BrokerChatCompletionChoice

## Properties

| Name              | Type                                                              | Description | Notes                          |
| ----------------- | ----------------------------------------------------------------- | ----------- | ------------------------------ |
| **index**         | **int**                                                           |             |
| **message**       | [**BrokerChatCompletionMessage**](BrokerChatCompletionMessage.md) |             |
| **finish_reason** | **str**                                                           |             | [optional] [default to 'stop'] |

## Example

```python
from kaziro.models.broker_chat_completion_choice import BrokerChatCompletionChoice

# TODO update the JSON string below
json = "{}"
# create an instance of BrokerChatCompletionChoice from a JSON string
broker_chat_completion_choice_instance = BrokerChatCompletionChoice.from_json(json)
# print the JSON string representation of the object
print(BrokerChatCompletionChoice.to_json())

# convert the object into a dict
broker_chat_completion_choice_dict = broker_chat_completion_choice_instance.to_dict()
# create an instance of BrokerChatCompletionChoice from a dict
broker_chat_completion_choice_from_dict = BrokerChatCompletionChoice.from_dict(broker_chat_completion_choice_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
