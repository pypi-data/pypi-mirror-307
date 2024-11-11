# ThreadMetadata

## Properties

| Name                        | Type    | Description | Notes      |
| --------------------------- | ------- | ----------- | ---------- |
| **status**                  | **str** |             | [optional] |
| **user_id**                 | **str** |             | [optional] |
| **processing_message_type** | **str** |             | [optional] |

## Example

```python
from kaziro.models.thread_metadata import ThreadMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of ThreadMetadata from a JSON string
thread_metadata_instance = ThreadMetadata.from_json(json)
# print the JSON string representation of the object
print(ThreadMetadata.to_json())

# convert the object into a dict
thread_metadata_dict = thread_metadata_instance.to_dict()
# create an instance of ThreadMetadata from a dict
thread_metadata_from_dict = ThreadMetadata.from_dict(thread_metadata_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
