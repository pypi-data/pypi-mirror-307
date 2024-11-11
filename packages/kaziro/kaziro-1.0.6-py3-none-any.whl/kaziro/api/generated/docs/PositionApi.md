# kaziro.PositionApi

All URIs are relative to _http://localhost_

| Method                                                                                                                | HTTP request                           | Description   |
| --------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ------------- |
| [**get_positions_v1_exchange_position_retrieve_get**](PositionApi.md#get_positions_v1_exchange_position_retrieve_get) | **GET** /v1/exchange/position/retrieve | Get positions |

# **get_positions_v1_exchange_position_retrieve_get**

> PositionResponse get_positions_v1_exchange_position_retrieve_get(status=status, page=page, sort_order=sort_order, include_markets=include_markets, include_orders=include_orders)

Get positions

Retrieve positions for the authenticated user.

### Example

-   Api Key Authentication (APIKeyHeader):

```python
import kaziro
from kaziro.models.position_response import PositionResponse
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
    api_instance = kaziro.PositionApi(api_client)
    status = 'ACTIVE' # str | Filter positions by status: 'ACTIVE', 'CLOSED' (optional) (default to 'ACTIVE')
    page = 1 # int | Page number for pagination. 100 positions per page. (optional) (default to 1)
    sort_order = 'ASC' # str | Sort order for results (ASC or DESC) (optional) (default to 'ASC')
    include_markets = False # bool |  (optional) (default to False)
    include_orders = False # bool |  (optional) (default to False)

    try:
        # Get positions
        api_response = api_instance.get_positions_v1_exchange_position_retrieve_get(status=status, page=page, sort_order=sort_order, include_markets=include_markets, include_orders=include_orders)
        print("The response of PositionApi->get_positions_v1_exchange_position_retrieve_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PositionApi->get_positions_v1_exchange_position_retrieve_get: %s\n" % e)
```

### Parameters

| Name                | Type     | Description                                                    | Notes                                    |
| ------------------- | -------- | -------------------------------------------------------------- | ---------------------------------------- |
| **status**          | **str**  | Filter positions by status: &#39;ACTIVE&#39;, &#39;CLOSED&#39; | [optional] [default to &#39;ACTIVE&#39;] |
| **page**            | **int**  | Page number for pagination. 100 positions per page.            | [optional] [default to 1]                |
| **sort_order**      | **str**  | Sort order for results (ASC or DESC)                           | [optional] [default to &#39;ASC&#39;]    |
| **include_markets** | **bool** |                                                                | [optional] [default to False]            |
| **include_orders**  | **bool** |                                                                | [optional] [default to False]            |

### Return type

[**PositionResponse**](PositionResponse.md)

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
