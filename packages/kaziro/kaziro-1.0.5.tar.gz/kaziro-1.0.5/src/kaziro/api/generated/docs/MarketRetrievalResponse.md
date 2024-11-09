# MarketRetrievalResponse

## Properties

| Name        | Type                          | Description | Notes |
| ----------- | ----------------------------- | ----------- | ----- |
| **markets** | [**List[Market]**](Market.md) |             |

## Example

```python
from kaziro.models.market_retrieval_response import MarketRetrievalResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MarketRetrievalResponse from a JSON string
market_retrieval_response_instance = MarketRetrievalResponse.from_json(json)
# print the JSON string representation of the object
print(MarketRetrievalResponse.to_json())

# convert the object into a dict
market_retrieval_response_dict = market_retrieval_response_instance.to_dict()
# create an instance of MarketRetrievalResponse from a dict
market_retrieval_response_from_dict = MarketRetrievalResponse.from_dict(market_retrieval_response_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
