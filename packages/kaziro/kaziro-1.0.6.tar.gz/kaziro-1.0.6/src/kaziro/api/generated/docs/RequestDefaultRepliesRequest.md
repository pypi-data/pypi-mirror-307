# RequestDefaultRepliesRequest

## Properties

| Name          | Type          | Description                                        | Notes |
| ------------- | ------------- | -------------------------------------------------- | ----- |
| **order_ids** | **List[str]** | List of request IDs to request default replies for |

## Example

```python
from kaziro.models.request_default_replies_request import RequestDefaultRepliesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RequestDefaultRepliesRequest from a JSON string
request_default_replies_request_instance = RequestDefaultRepliesRequest.from_json(json)
# print the JSON string representation of the object
print(RequestDefaultRepliesRequest.to_json())

# convert the object into a dict
request_default_replies_request_dict = request_default_replies_request_instance.to_dict()
# create an instance of RequestDefaultRepliesRequest from a dict
request_default_replies_request_from_dict = RequestDefaultRepliesRequest.from_dict(request_default_replies_request_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
