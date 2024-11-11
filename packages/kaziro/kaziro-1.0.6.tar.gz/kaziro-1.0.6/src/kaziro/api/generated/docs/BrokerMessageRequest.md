# BrokerMessageRequest

## Properties

| Name              | Type                                                                    | Description | Notes      |
| ----------------- | ----------------------------------------------------------------------- | ----------- | ---------- |
| **model**         | **str**                                                                 |             |
| **messages**      | [**List[BrokerChatCompletionMessage]**](BrokerChatCompletionMessage.md) |             |
| **thread_id**     | **str**                                                                 |             | [optional] |
| **extra_headers** | **object**                                                              |             | [optional] |

## Example

```python
from kaziro.models.broker_message_request import BrokerMessageRequest

# TODO update the JSON string below
json = "{}"
# create an instance of BrokerMessageRequest from a JSON string
broker_message_request_instance = BrokerMessageRequest.from_json(json)
# print the JSON string representation of the object
print(BrokerMessageRequest.to_json())

# convert the object into a dict
broker_message_request_dict = broker_message_request_instance.to_dict()
# create an instance of BrokerMessageRequest from a dict
broker_message_request_from_dict = BrokerMessageRequest.from_dict(broker_message_request_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
