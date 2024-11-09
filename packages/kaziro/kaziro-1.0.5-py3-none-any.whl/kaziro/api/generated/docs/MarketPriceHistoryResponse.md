# MarketPriceHistoryResponse

## Properties

| Name        | Type                                          | Description | Notes |
| ----------- | --------------------------------------------- | ----------- | ----- |
| **markets** | [**List[MarketOHLCData]**](MarketOHLCData.md) |             |

## Example

```python
from kaziro.models.market_price_history_response import MarketPriceHistoryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MarketPriceHistoryResponse from a JSON string
market_price_history_response_instance = MarketPriceHistoryResponse.from_json(json)
# print the JSON string representation of the object
print(MarketPriceHistoryResponse.to_json())

# convert the object into a dict
market_price_history_response_dict = market_price_history_response_instance.to_dict()
# create an instance of MarketPriceHistoryResponse from a dict
market_price_history_response_from_dict = MarketPriceHistoryResponse.from_dict(market_price_history_response_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
