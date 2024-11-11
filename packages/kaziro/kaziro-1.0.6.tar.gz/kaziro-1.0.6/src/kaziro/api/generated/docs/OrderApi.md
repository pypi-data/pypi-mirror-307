# kaziro.OrderApi

All URIs are relative to _http://localhost_

| Method                                                                                                                                                             | HTTP request                                | Description             |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------- | ----------------------- |
| [**accept_orders_endpoint_v1_exchange_order_accept_post**](OrderApi.md#accept_orders_endpoint_v1_exchange_order_accept_post)                                       | **POST** /v1/exchange/order/accept          | Accept orders           |
| [**create_market_endpoint_v1_exchange_order_create_post**](OrderApi.md#create_market_endpoint_v1_exchange_order_create_post)                                       | **POST** /v1/exchange/order/create          | Place multiple orders   |
| [**get_open_orders_endpoint_v1_exchange_order_retrieve_get**](OrderApi.md#get_open_orders_endpoint_v1_exchange_order_retrieve_get)                                 | **GET** /v1/exchange/order/retrieve         | Retrieve open orders    |
| [**request_default_replies_endpoint_v1_exchange_order_temporary_reply_post**](OrderApi.md#request_default_replies_endpoint_v1_exchange_order_temporary_reply_post) | **POST** /v1/exchange/order/temporary/reply | Request default replies |

# **accept_orders_endpoint_v1_exchange_order_accept_post**

> AcceptOrdersResponse accept_orders_endpoint_v1_exchange_order_accept_post(accept_orders_request)

Accept orders

Accept multiple open orders for the authenticated user.

### Example

-   Api Key Authentication (APIKeyHeader):

```python
import kaziro
from kaziro.models.accept_orders_request import AcceptOrdersRequest
from kaziro.models.accept_orders_response import AcceptOrdersResponse
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
    api_instance = kaziro.OrderApi(api_client)
    accept_orders_request = kaziro.AcceptOrdersRequest() # AcceptOrdersRequest |

    try:
        # Accept orders
        api_response = api_instance.accept_orders_endpoint_v1_exchange_order_accept_post(accept_orders_request)
        print("The response of OrderApi->accept_orders_endpoint_v1_exchange_order_accept_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrderApi->accept_orders_endpoint_v1_exchange_order_accept_post: %s\n" % e)
```

### Parameters

| Name                      | Type                                              | Description | Notes |
| ------------------------- | ------------------------------------------------- | ----------- | ----- |
| **accept_orders_request** | [**AcceptOrdersRequest**](AcceptOrdersRequest.md) |             |

### Return type

[**AcceptOrdersResponse**](AcceptOrdersResponse.md)

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
| **406**     | Not Acceptable        | -                |
| **422**     | Validation Error      | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_market_endpoint_v1_exchange_order_create_post**

> PlaceOrderResponse create_market_endpoint_v1_exchange_order_create_post(order_request)

Place multiple orders

Create multiple market reply orders for the authenticated user.

### Example

-   Api Key Authentication (APIKeyHeader):

```python
import kaziro
from kaziro.models.order_request import OrderRequest
from kaziro.models.place_order_response import PlaceOrderResponse
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
    api_instance = kaziro.OrderApi(api_client)
    order_request = [kaziro.OrderRequest()] # List[OrderRequest] |

    try:
        # Place multiple orders
        api_response = api_instance.create_market_endpoint_v1_exchange_order_create_post(order_request)
        print("The response of OrderApi->create_market_endpoint_v1_exchange_order_create_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrderApi->create_market_endpoint_v1_exchange_order_create_post: %s\n" % e)
```

### Parameters

| Name              | Type                                      | Description | Notes |
| ----------------- | ----------------------------------------- | ----------- | ----- |
| **order_request** | [**List[OrderRequest]**](OrderRequest.md) |             |

### Return type

[**PlaceOrderResponse**](PlaceOrderResponse.md)

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

# **get_open_orders_endpoint_v1_exchange_order_retrieve_get**

> OpenOrdersResponse get_open_orders_endpoint_v1_exchange_order_retrieve_get(order_ids=order_ids, market_ids=market_ids, outcome=outcome, filter_user=filter_user, include_markets=include_markets, include_creators=include_creators)

Retrieve open orders

Get open orders, optionally filtered by market IDs and user.

### Example

-   Api Key Authentication (APIKeyHeader):

```python
import kaziro
from kaziro.models.open_orders_response import OpenOrdersResponse
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
    api_instance = kaziro.OrderApi(api_client)
    order_ids = ['order_ids_example'] # List[str] |  (optional)
    market_ids = ['market_ids_example'] # List[str] |  (optional)
    outcome = 56 # int |  (optional)
    filter_user = False # bool |  (optional) (default to False)
    include_markets = False # bool |  (optional) (default to False)
    include_creators = False # bool |  (optional) (default to False)

    try:
        # Retrieve open orders
        api_response = api_instance.get_open_orders_endpoint_v1_exchange_order_retrieve_get(order_ids=order_ids, market_ids=market_ids, outcome=outcome, filter_user=filter_user, include_markets=include_markets, include_creators=include_creators)
        print("The response of OrderApi->get_open_orders_endpoint_v1_exchange_order_retrieve_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrderApi->get_open_orders_endpoint_v1_exchange_order_retrieve_get: %s\n" % e)
```

### Parameters

| Name                 | Type                    | Description | Notes                         |
| -------------------- | ----------------------- | ----------- | ----------------------------- |
| **order_ids**        | [**List[str]**](str.md) |             | [optional]                    |
| **market_ids**       | [**List[str]**](str.md) |             | [optional]                    |
| **outcome**          | **int**                 |             | [optional]                    |
| **filter_user**      | **bool**                |             | [optional] [default to False] |
| **include_markets**  | **bool**                |             | [optional] [default to False] |
| **include_creators** | **bool**                |             | [optional] [default to False] |

### Return type

[**OpenOrdersResponse**](OpenOrdersResponse.md)

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
| **500**     | Internal Server Error | -                |
| **422**     | Validation Error      | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **request_default_replies_endpoint_v1_exchange_order_temporary_reply_post**

> RequestDefaultRepliesResponse request_default_replies_endpoint_v1_exchange_order_temporary_reply_post(request_default_replies_request)

Request default replies

Request default replies for multiple open requests.

### Example

-   Api Key Authentication (APIKeyHeader):

```python
import kaziro
from kaziro.models.request_default_replies_request import RequestDefaultRepliesRequest
from kaziro.models.request_default_replies_response import RequestDefaultRepliesResponse
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
    api_instance = kaziro.OrderApi(api_client)
    request_default_replies_request = kaziro.RequestDefaultRepliesRequest() # RequestDefaultRepliesRequest |

    try:
        # Request default replies
        api_response = api_instance.request_default_replies_endpoint_v1_exchange_order_temporary_reply_post(request_default_replies_request)
        print("The response of OrderApi->request_default_replies_endpoint_v1_exchange_order_temporary_reply_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrderApi->request_default_replies_endpoint_v1_exchange_order_temporary_reply_post: %s\n" % e)
```

### Parameters

| Name                                | Type                                                                | Description | Notes |
| ----------------------------------- | ------------------------------------------------------------------- | ----------- | ----- |
| **request_default_replies_request** | [**RequestDefaultRepliesRequest**](RequestDefaultRepliesRequest.md) |             |

### Return type

[**RequestDefaultRepliesResponse**](RequestDefaultRepliesResponse.md)

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
