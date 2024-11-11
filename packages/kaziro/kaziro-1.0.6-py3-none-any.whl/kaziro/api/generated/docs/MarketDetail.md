# MarketDetail

## Properties

| Name       | Type    | Description | Notes      |
| ---------- | ------- | ----------- | ---------- |
| **detail** | **str** |             |
| **ref_id** | **str** |             | [optional] |

## Example

```python
from kaziro.models.market_detail import MarketDetail

# TODO update the JSON string below
json = "{}"
# create an instance of MarketDetail from a JSON string
market_detail_instance = MarketDetail.from_json(json)
# print the JSON string representation of the object
print(MarketDetail.to_json())

# convert the object into a dict
market_detail_dict = market_detail_instance.to_dict()
# create an instance of MarketDetail from a dict
market_detail_from_dict = MarketDetail.from_dict(market_detail_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
