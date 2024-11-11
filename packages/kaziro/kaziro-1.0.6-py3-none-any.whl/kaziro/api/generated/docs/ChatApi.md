# kaziro.ChatApi

All URIs are relative to _http://localhost_

| Method                                                                                                                                        | HTTP request                       | Description                     |
| --------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- | ------------------------------- |
| [**create_chat_message_endpoint_v1_exchange_chat_create_post**](ChatApi.md#create_chat_message_endpoint_v1_exchange_chat_create_post)         | **POST** /v1/exchange/chat/create  | Create Chat Message Endpoint    |
| [**retrieve_chat_messages_endpoint_v1_exchange_chat_retrieve_get**](ChatApi.md#retrieve_chat_messages_endpoint_v1_exchange_chat_retrieve_get) | **GET** /v1/exchange/chat/retrieve | Retrieve Chat Messages Endpoint |

# **create_chat_message_endpoint_v1_exchange_chat_create_post**

> Chat create_chat_message_endpoint_v1_exchange_chat_create_post(chat_creation_request)

Create Chat Message Endpoint

Create a new chat message.

### Example

-   Api Key Authentication (APIKeyHeader):

```python
import kaziro
from kaziro.models.chat import Chat
from kaziro.models.chat_creation_request import ChatCreationRequest
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
    api_instance = kaziro.ChatApi(api_client)
    chat_creation_request = kaziro.ChatCreationRequest() # ChatCreationRequest |

    try:
        # Create Chat Message Endpoint
        api_response = api_instance.create_chat_message_endpoint_v1_exchange_chat_create_post(chat_creation_request)
        print("The response of ChatApi->create_chat_message_endpoint_v1_exchange_chat_create_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->create_chat_message_endpoint_v1_exchange_chat_create_post: %s\n" % e)
```

### Parameters

| Name                      | Type                                              | Description | Notes |
| ------------------------- | ------------------------------------------------- | ----------- | ----- |
| **chat_creation_request** | [**ChatCreationRequest**](ChatCreationRequest.md) |             |

### Return type

[**Chat**](Chat.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

-   **Content-Type**: application/json
-   **Accept**: application/json

### HTTP response details

| Status code | Description           | Response headers |
| ----------- | --------------------- | ---------------- |
| **200**     | Successful Response   | -                |
| **400**     | Bad Request           | -                |
| **500**     | Internal Server Error | -                |
| **422**     | Validation Error      | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_chat_messages_endpoint_v1_exchange_chat_retrieve_get**

> ChatRetrievalResponse retrieve_chat_messages_endpoint_v1_exchange_chat_retrieve_get(market_id=market_id, order_id=order_id, user_id=user_id, is_global=is_global, limit=limit, before_date=before_date, include_market=include_market, include_user=include_user)

Retrieve Chat Messages Endpoint

Retrieve chat messages with optional related data.

### Example

```python
import kaziro
from kaziro.models.chat_retrieval_response import ChatRetrievalResponse
from kaziro.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = kaziro.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with kaziro.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = kaziro.ChatApi(api_client)
    market_id = 'market_id_example' # str |  (optional)
    order_id = 'order_id_example' # str |  (optional)
    user_id = 'user_id_example' # str |  (optional)
    is_global = True # bool |  (optional)
    limit = 100 # int |  (optional) (default to 100)
    before_date = 'before_date_example' # str |  (optional)
    include_market = False # bool | Include full market data in response (optional) (default to False)
    include_user = False # bool | Include full user data in response (optional) (default to False)

    try:
        # Retrieve Chat Messages Endpoint
        api_response = api_instance.retrieve_chat_messages_endpoint_v1_exchange_chat_retrieve_get(market_id=market_id, order_id=order_id, user_id=user_id, is_global=is_global, limit=limit, before_date=before_date, include_market=include_market, include_user=include_user)
        print("The response of ChatApi->retrieve_chat_messages_endpoint_v1_exchange_chat_retrieve_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->retrieve_chat_messages_endpoint_v1_exchange_chat_retrieve_get: %s\n" % e)
```

### Parameters

| Name               | Type     | Description                          | Notes                         |
| ------------------ | -------- | ------------------------------------ | ----------------------------- |
| **market_id**      | **str**  |                                      | [optional]                    |
| **order_id**       | **str**  |                                      | [optional]                    |
| **user_id**        | **str**  |                                      | [optional]                    |
| **is_global**      | **bool** |                                      | [optional]                    |
| **limit**          | **int**  |                                      | [optional] [default to 100]   |
| **before_date**    | **str**  |                                      | [optional]                    |
| **include_market** | **bool** | Include full market data in response | [optional] [default to False] |
| **include_user**   | **bool** | Include full user data in response   | [optional] [default to False] |

### Return type

[**ChatRetrievalResponse**](ChatRetrievalResponse.md)

### Authorization

No authorization required

### HTTP request headers

-   **Content-Type**: Not defined
-   **Accept**: application/json

### HTTP response details

| Status code | Description           | Response headers |
| ----------- | --------------------- | ---------------- |
| **200**     | Successful Response   | -                |
| **400**     | Bad Request           | -                |
| **500**     | Internal Server Error | -                |
| **422**     | Validation Error      | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
