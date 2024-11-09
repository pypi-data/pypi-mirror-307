# UserProfile

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
from kaziro.models.user_profile import UserProfile

# TODO update the JSON string below
json = "{}"
# create an instance of UserProfile from a JSON string
user_profile_instance = UserProfile.from_json(json)
# print the JSON string representation of the object
print(UserProfile.to_json())

# convert the object into a dict
user_profile_dict = user_profile_instance.to_dict()
# create an instance of UserProfile from a dict
user_profile_from_dict = UserProfile.from_dict(user_profile_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
