# PositionWithMarketAndOrders

## Properties

| Name                    | Type                    | Description                                                                                                         | Notes      |
| ----------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------- | ---------- |
| **id**                  | **str**                 | Unique identifier for the position                                                                                  |
| **market_id**           | **str**                 | ID of the market this position belongs to                                                                           |
| **status**              | **str**                 | Status of the position                                                                                              |
| **side**                | **str**                 | Side of the position based on the caller&#39;s user_id                                                              |
| **request_size**        | **float**               | Size of the request order                                                                                           |
| **request_id**          | **str**                 | ID of the request order (order_id)                                                                                  | [optional] |
| **reply_size**          | **float**               | Size of the reply order                                                                                             |
| **reply_id**            | **str**                 | ID of the reply order (order_id)                                                                                    | [optional] |
| **protocol_id**         | **int**                 | On-chain ID of the position                                                                                         |
| **metadata**            | **object**              | Additional metadata for the position                                                                                | [optional] |
| **outcome**             | **int**                 | Result of the position. 1 for outcome 1, 2 for outcome 2, 0 for not yet determined, 3 for void                      | [optional] |
| **outcome_probability** | **float**               | Probability of outcome 1. Provided for convenience. Can be determined from the size of the request and reply orders | [optional] |
| **market**              | [**Market**](Market.md) | The market of the position                                                                                          | [optional] |
| **request_order**       | [**Order**](Order.md)   | The request order of the position                                                                                   | [optional] |
| **reply_order**         | [**Order**](Order.md)   | The reply order of the position                                                                                     | [optional] |

## Example

```python
from kaziro.models.position_with_market_and_orders import PositionWithMarketAndOrders

# TODO update the JSON string below
json = "{}"
# create an instance of PositionWithMarketAndOrders from a JSON string
position_with_market_and_orders_instance = PositionWithMarketAndOrders.from_json(json)
# print the JSON string representation of the object
print(PositionWithMarketAndOrders.to_json())

# convert the object into a dict
position_with_market_and_orders_dict = position_with_market_and_orders_instance.to_dict()
# create an instance of PositionWithMarketAndOrders from a dict
position_with_market_and_orders_from_dict = PositionWithMarketAndOrders.from_dict(position_with_market_and_orders_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
