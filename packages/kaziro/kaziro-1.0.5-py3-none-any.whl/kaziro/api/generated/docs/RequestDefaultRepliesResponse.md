# RequestDefaultRepliesResponse

## Properties

| Name        | Type                                                | Description                                     | Notes |
| ----------- | --------------------------------------------------- | ----------------------------------------------- | ----- |
| **success** | **bool**                                            | Indicates if the operation was successful.      |
| **message** | **str**                                             | Descriptive message about the operation result. |
| **orders**  | [**List[DefaultReplyOrder]**](DefaultReplyOrder.md) | List of default replies for the markets.        |

## Example

```python
from kaziro.models.request_default_replies_response import RequestDefaultRepliesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RequestDefaultRepliesResponse from a JSON string
request_default_replies_response_instance = RequestDefaultRepliesResponse.from_json(json)
# print the JSON string representation of the object
print(RequestDefaultRepliesResponse.to_json())

# convert the object into a dict
request_default_replies_response_dict = request_default_replies_response_instance.to_dict()
# create an instance of RequestDefaultRepliesResponse from a dict
request_default_replies_response_from_dict = RequestDefaultRepliesResponse.from_dict(request_default_replies_response_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
