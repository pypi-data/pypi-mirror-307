# UserRetrievalResponse

## Properties

| Name        | Type                      | Description                                    | Notes |
| ----------- | ------------------------- | ---------------------------------------------- | ----- |
| **success** | **bool**                  | Indicates if the operation was successful      |
| **message** | **str**                   | Descriptive message about the operation result |
| **users**   | [**List[User]**](User.md) | List of user profiles                          |

## Example

```python
from kaziro.models.user_retrieval_response import UserRetrievalResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UserRetrievalResponse from a JSON string
user_retrieval_response_instance = UserRetrievalResponse.from_json(json)
# print the JSON string representation of the object
print(UserRetrievalResponse.to_json())

# convert the object into a dict
user_retrieval_response_dict = user_retrieval_response_instance.to_dict()
# create an instance of UserRetrievalResponse from a dict
user_retrieval_response_from_dict = UserRetrievalResponse.from_dict(user_retrieval_response_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
