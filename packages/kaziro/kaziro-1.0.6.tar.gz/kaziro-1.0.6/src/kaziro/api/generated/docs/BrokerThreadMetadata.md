# BrokerThreadMetadata

## Properties

| Name                        | Type    | Description | Notes      |
| --------------------------- | ------- | ----------- | ---------- |
| **status**                  | **str** |             | [optional] |
| **user_id**                 | **str** |             | [optional] |
| **processing_message_type** | **str** |             | [optional] |

## Example

```python
from kaziro.models.broker_thread_metadata import BrokerThreadMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of BrokerThreadMetadata from a JSON string
broker_thread_metadata_instance = BrokerThreadMetadata.from_json(json)
# print the JSON string representation of the object
print(BrokerThreadMetadata.to_json())

# convert the object into a dict
broker_thread_metadata_dict = broker_thread_metadata_instance.to_dict()
# create an instance of BrokerThreadMetadata from a dict
broker_thread_metadata_from_dict = BrokerThreadMetadata.from_dict(broker_thread_metadata_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
