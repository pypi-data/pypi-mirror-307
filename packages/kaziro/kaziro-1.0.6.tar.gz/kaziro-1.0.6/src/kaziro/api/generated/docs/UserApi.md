# kaziro.UserApi

All URIs are relative to _http://localhost_

| Method                                                                                                          | HTTP request              | Description               |
| --------------------------------------------------------------------------------------------------------------- | ------------------------- | ------------------------- |
| [**profile_retrieve_endpoint_v1_user_retrieve_get**](UserApi.md#profile_retrieve_endpoint_v1_user_retrieve_get) | **GET** /v1/user/retrieve | Profile Retrieve Endpoint |

# **profile_retrieve_endpoint_v1_user_retrieve_get**

> UserRetrievalResponse profile_retrieve_endpoint_v1_user_retrieve_get(user_ids=user_ids, usernames=usernames)

Profile Retrieve Endpoint

Retrieve user profiles by either user IDs or usernames. Parameters: - user_ids: Optional list of user IDs - usernames: Optional list of usernames If no user_ids or usernames are provided, the user profile for the authenticated user will be retrieved. If no authenticated user is provided, an error will be returned. Returns profiles for the requested users. Must provide either user_ids or usernames.

### Example

-   Api Key Authentication (APIKeyHeader):

```python
import kaziro
from kaziro.models.user_retrieval_response import UserRetrievalResponse
from kaziro.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = kaziro.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyHeader
configuration.api_key['APIKeyHeader'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyHeader'] = 'Bearer'

# Enter a context with an instance of the API client
with kaziro.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = kaziro.UserApi(api_client)
    user_ids = ['user_ids_example'] # List[str] | List of user IDs to retrieve profiles for (optional)
    usernames = ['usernames_example'] # List[str] | List of usernames to retrieve profiles for (optional)

    try:
        # Profile Retrieve Endpoint
        api_response = api_instance.profile_retrieve_endpoint_v1_user_retrieve_get(user_ids=user_ids, usernames=usernames)
        print("The response of UserApi->profile_retrieve_endpoint_v1_user_retrieve_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->profile_retrieve_endpoint_v1_user_retrieve_get: %s\n" % e)
```

### Parameters

| Name          | Type                    | Description                                | Notes      |
| ------------- | ----------------------- | ------------------------------------------ | ---------- |
| **user_ids**  | [**List[str]**](str.md) | List of user IDs to retrieve profiles for  | [optional] |
| **usernames** | [**List[str]**](str.md) | List of usernames to retrieve profiles for | [optional] |

### Return type

[**UserRetrievalResponse**](UserRetrievalResponse.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

-   **Content-Type**: Not defined
-   **Accept**: application/json

### HTTP response details

| Status code | Description           | Response headers |
| ----------- | --------------------- | ---------------- |
| **200**     | Successful Response   | -                |
| **400**     | Bad Request           | -                |
| **404**     | Not Found             | -                |
| **500**     | Internal Server Error | -                |
| **422**     | Validation Error      | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
