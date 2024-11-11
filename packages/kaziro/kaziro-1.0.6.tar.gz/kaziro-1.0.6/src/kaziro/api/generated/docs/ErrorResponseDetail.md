# ErrorResponseDetail

## Properties

| Name            | Type    | Description | Notes                           |
| --------------- | ------- | ----------- | ------------------------------- |
| **status**      | **str** |             | [optional] [default to 'error'] |
| **status_code** | **int** |             |
| **message**     | **str** |             |

## Example

```python
from kaziro.models.error_response_detail import ErrorResponseDetail

# TODO update the JSON string below
json = "{}"
# create an instance of ErrorResponseDetail from a JSON string
error_response_detail_instance = ErrorResponseDetail.from_json(json)
# print the JSON string representation of the object
print(ErrorResponseDetail.to_json())

# convert the object into a dict
error_response_detail_dict = error_response_detail_instance.to_dict()
# create an instance of ErrorResponseDetail from a dict
error_response_detail_from_dict = ErrorResponseDetail.from_dict(error_response_detail_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
