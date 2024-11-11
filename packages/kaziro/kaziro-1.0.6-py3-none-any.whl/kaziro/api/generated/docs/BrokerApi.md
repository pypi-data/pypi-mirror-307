# kaziro.BrokerApi

All URIs are relative to _http://localhost_

| Method                                                                                                                                        | HTTP request                         | Description                  |
| --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ | ---------------------------- |
| [**create_chat_message_endpoint_v1_broker_chat_completions_post**](BrokerApi.md#create_chat_message_endpoint_v1_broker_chat_completions_post) | **POST** /v1/broker/chat/completions | Create Chat Message Endpoint |
| [**create_thread_endpoint_v1_broker_thread_create_post**](BrokerApi.md#create_thread_endpoint_v1_broker_thread_create_post)                   | **POST** /v1/broker/thread/create    | Create Thread Endpoint       |
| [**get_thread_metadata_endpoint_v1_broker_thread_retrieve_get**](BrokerApi.md#get_thread_metadata_endpoint_v1_broker_thread_retrieve_get)     | **GET** /v1/broker/thread/retrieve   | Get Thread Metadata Endpoint |

# **create_chat_message_endpoint_v1_broker_chat_completions_post**

> BrokerChatCompletionResponse create_chat_message_endpoint_v1_broker_chat_completions_post(broker_message_request)

Create Chat Message Endpoint

### Example

-   Api Key Authentication (APIKeyHeader):

```python
import kaziro
from kaziro.models.broker_chat_completion_response import BrokerChatCompletionResponse
from kaziro.models.broker_message_request import BrokerMessageRequest
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
    api_instance = kaziro.BrokerApi(api_client)
    broker_message_request = kaziro.BrokerMessageRequest() # BrokerMessageRequest |

    try:
        # Create Chat Message Endpoint
        api_response = api_instance.create_chat_message_endpoint_v1_broker_chat_completions_post(broker_message_request)
        print("The response of BrokerApi->create_chat_message_endpoint_v1_broker_chat_completions_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrokerApi->create_chat_message_endpoint_v1_broker_chat_completions_post: %s\n" % e)
```

### Parameters

| Name                       | Type                                                | Description | Notes |
| -------------------------- | --------------------------------------------------- | ----------- | ----- |
| **broker_message_request** | [**BrokerMessageRequest**](BrokerMessageRequest.md) |             |

### Return type

[**BrokerChatCompletionResponse**](BrokerChatCompletionResponse.md)

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

# **create_thread_endpoint_v1_broker_thread_create_post**

> BrokerThreadCreateResponse create_thread_endpoint_v1_broker_thread_create_post()

Create Thread Endpoint

### Example

-   Api Key Authentication (APIKeyHeader):

```python
import kaziro
from kaziro.models.broker_thread_create_response import BrokerThreadCreateResponse
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
    api_instance = kaziro.BrokerApi(api_client)

    try:
        # Create Thread Endpoint
        api_response = api_instance.create_thread_endpoint_v1_broker_thread_create_post()
        print("The response of BrokerApi->create_thread_endpoint_v1_broker_thread_create_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrokerApi->create_thread_endpoint_v1_broker_thread_create_post: %s\n" % e)
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**BrokerThreadCreateResponse**](BrokerThreadCreateResponse.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

-   **Content-Type**: Not defined
-   **Accept**: application/json

### HTTP response details

| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **200**     | Successful Response | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_thread_metadata_endpoint_v1_broker_thread_retrieve_get**

> BrokerThreadMetadata get_thread_metadata_endpoint_v1_broker_thread_retrieve_get(thread_id)

Get Thread Metadata Endpoint

### Example

```python
import kaziro
from kaziro.models.broker_thread_metadata import BrokerThreadMetadata
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
    api_instance = kaziro.BrokerApi(api_client)
    thread_id = 'thread_id_example' # str |

    try:
        # Get Thread Metadata Endpoint
        api_response = api_instance.get_thread_metadata_endpoint_v1_broker_thread_retrieve_get(thread_id)
        print("The response of BrokerApi->get_thread_metadata_endpoint_v1_broker_thread_retrieve_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrokerApi->get_thread_metadata_endpoint_v1_broker_thread_retrieve_get: %s\n" % e)
```

### Parameters

| Name          | Type    | Description | Notes |
| ------------- | ------- | ----------- | ----- |
| **thread_id** | **str** |             |

### Return type

[**BrokerThreadMetadata**](BrokerThreadMetadata.md)

### Authorization

No authorization required

### HTTP request headers

-   **Content-Type**: Not defined
-   **Accept**: application/json

### HTTP response details

| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **200**     | Successful Response | -                |
| **422**     | Validation Error    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
