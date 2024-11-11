# ThreadCreateResponse

## Properties

| Name          | Type    | Description | Notes |
| ------------- | ------- | ----------- | ----- |
| **thread_id** | **str** |             |

## Example

```python
from kaziro.models.thread_create_response import ThreadCreateResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ThreadCreateResponse from a JSON string
thread_create_response_instance = ThreadCreateResponse.from_json(json)
# print the JSON string representation of the object
print(ThreadCreateResponse.to_json())

# convert the object into a dict
thread_create_response_dict = thread_create_response_instance.to_dict()
# create an instance of ThreadCreateResponse from a dict
thread_create_response_from_dict = ThreadCreateResponse.from_dict(thread_create_response_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
