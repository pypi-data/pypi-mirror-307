# MarketCreationResponseMarketsInner

## Properties

| Name             | Type          | Description                                                           | Notes                           |
| ---------------- | ------------- | --------------------------------------------------------------------- | ------------------------------- |
| **id**           | **str**       | Unique identifier for the market                                      |
| **date_created** | **str**       | The date the market was created                                       |
| **question**     | **str**       | The question of the market                                            |
| **outcome_1**    | **str**       | The first outcome of the market                                       |
| **outcome_2**    | **str**       | The second outcome of the market                                      |
| **description**  | **str**       | The description of the market                                         |
| **end_date**     | **str**       | The end date of the market                                            | [optional]                      |
| **tags**         | **List[str]** | The tags of the market                                                | [optional]                      |
| **creator_id**   | **str**       | The creator of the market                                             | [optional]                      |
| **date_closed**  | **str**       | The date the market was closed                                        | [optional]                      |
| **result**       | **str**       | The result of the market. One of None, outcome_1, outcome_2, or void. | [optional]                      |
| **ref_id**       | **str**       | The reference identifier of the market                                | [optional]                      |
| **status**       | **str**       |                                                                       | [optional] [default to 'error'] |
| **status_code**  | **int**       |                                                                       |
| **message**      | **str**       |                                                                       |

## Example

```python
from kaziro.models.market_creation_response_markets_inner import MarketCreationResponseMarketsInner

# TODO update the JSON string below
json = "{}"
# create an instance of MarketCreationResponseMarketsInner from a JSON string
market_creation_response_markets_inner_instance = MarketCreationResponseMarketsInner.from_json(json)
# print the JSON string representation of the object
print(MarketCreationResponseMarketsInner.to_json())

# convert the object into a dict
market_creation_response_markets_inner_dict = market_creation_response_markets_inner_instance.to_dict()
# create an instance of MarketCreationResponseMarketsInner from a dict
market_creation_response_markets_inner_from_dict = MarketCreationResponseMarketsInner.from_dict(market_creation_response_markets_inner_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
