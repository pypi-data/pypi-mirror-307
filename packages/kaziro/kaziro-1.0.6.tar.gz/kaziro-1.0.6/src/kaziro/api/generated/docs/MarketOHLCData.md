# MarketOHLCData

## Properties

| Name                    | Type                              | Description | Notes |
| ----------------------- | --------------------------------- | ----------- | ----- |
| **market_id**           | **str**                           |             |
| **outcome_1_ohlc_data** | [**List[OHLCData]**](OHLCData.md) |             |
| **outcome_2_ohlc_data** | [**List[OHLCData]**](OHLCData.md) |             |

## Example

```python
from kaziro.models.market_ohlc_data import MarketOHLCData

# TODO update the JSON string below
json = "{}"
# create an instance of MarketOHLCData from a JSON string
market_ohlc_data_instance = MarketOHLCData.from_json(json)
# print the JSON string representation of the object
print(MarketOHLCData.to_json())

# convert the object into a dict
market_ohlc_data_dict = market_ohlc_data_instance.to_dict()
# create an instance of MarketOHLCData from a dict
market_ohlc_data_from_dict = MarketOHLCData.from_dict(market_ohlc_data_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
