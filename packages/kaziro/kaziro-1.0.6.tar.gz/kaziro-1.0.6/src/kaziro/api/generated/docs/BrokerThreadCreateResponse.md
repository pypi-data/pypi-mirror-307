# BrokerThreadCreateResponse

## Properties

| Name          | Type    | Description | Notes |
| ------------- | ------- | ----------- | ----- |
| **thread_id** | **str** |             |

## Example

```python
from kaziro.models.broker_thread_create_response import BrokerThreadCreateResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BrokerThreadCreateResponse from a JSON string
broker_thread_create_response_instance = BrokerThreadCreateResponse.from_json(json)
# print the JSON string representation of the object
print(BrokerThreadCreateResponse.to_json())

# convert the object into a dict
broker_thread_create_response_dict = broker_thread_create_response_instance.to_dict()
# create an instance of BrokerThreadCreateResponse from a dict
broker_thread_create_response_from_dict = BrokerThreadCreateResponse.from_dict(broker_thread_create_response_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
