# MarketCreationResponse

## Properties

| Name        | Type                          | Description | Notes |
| ----------- | ----------------------------- | ----------- | ----- |
| **markets** | [**List[Market]**](Market.md) |             |

## Example

```python
from kaziro.models.market_creation_response import MarketCreationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MarketCreationResponse from a JSON string
market_creation_response_instance = MarketCreationResponse.from_json(json)
# print the JSON string representation of the object
print(MarketCreationResponse.to_json())

# convert the object into a dict
market_creation_response_dict = market_creation_response_instance.to_dict()
# create an instance of MarketCreationResponse from a dict
market_creation_response_from_dict = MarketCreationResponse.from_dict(market_creation_response_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
