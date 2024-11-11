# User

## Properties

| Name                | Type       | Description                        | Notes      |
| ------------------- | ---------- | ---------------------------------- | ---------- |
| **id**              | **str**    | Unique identifier for the user     |
| **date_created**    | **str**    | Timestamp of user account creation |
| **username**        | **str**    | User&#39;s chosen username         |
| **display_name**    | **str**    | User&#39;s display name            | [optional] |
| **profile_picture** | **str**    | URL to user&#39;s profile picture  | [optional] |
| **metadata**        | **object** | Additional metadata for the user   | [optional] |
| **user_type**       | **str**    | Type of user account               | [optional] |
| **bio**             | **str**    | User&#39;s biography               | [optional] |

## Example

```python
from kaziro.models.user import User

# TODO update the JSON string below
json = "{}"
# create an instance of User from a JSON string
user_instance = User.from_json(json)
# print the JSON string representation of the object
print(User.to_json())

# convert the object into a dict
user_dict = user_instance.to_dict()
# create an instance of User from a dict
user_from_dict = User.from_dict(user_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
