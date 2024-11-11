# OrderRequest

## Properties

| Name            | Type      | Description                                                                        | Notes                     |
| --------------- | --------- | ---------------------------------------------------------------------------------- | ------------------------- |
| **order_type**  | **str**   | Type of order. MARKET_REPLY or MARKET_REQUEST                                      |
| **outcome**     | **int**   | Outcome of the order. 1 for outcome 1, 2 for outcome 2.                            | [optional] [default to 1] |
| **size**        | **float** | Size of the order. Only required for MARKET_REQUEST orders.                        | [optional]                |
| **market_id**   | **str**   | Unique identifier for the market. Only required for MARKET_REQUEST orders.         | [optional]                |
| **request_id**  | **str**   | Unique identifier for the market. Only required for MARKET_REPLY orders.           | [optional]                |
| **probability** | **float** | Probability for the order, between 0 and 1. Only required for MARKET_REPLY orders. | [optional]                |

## Example

```python
from kaziro.models.order_request import OrderRequest

# TODO update the JSON string below
json = "{}"
# create an instance of OrderRequest from a JSON string
order_request_instance = OrderRequest.from_json(json)
# print the JSON string representation of the object
print(OrderRequest.to_json())

# convert the object into a dict
order_request_dict = order_request_instance.to_dict()
# create an instance of OrderRequest from a dict
order_request_from_dict = OrderRequest.from_dict(order_request_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
