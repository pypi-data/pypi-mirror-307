# Market

## Properties

| Name             | Type          | Description                                                                         | Notes      |
| ---------------- | ------------- | ----------------------------------------------------------------------------------- | ---------- |
| **id**           | **str**       | Unique identifier for the market                                                    |
| **date_created** | **str**       | The date the market was created                                                     |
| **question**     | **str**       | The question of the market                                                          |
| **outcome_1**    | **str**       | The first outcome of the market                                                     |
| **outcome_2**    | **str**       | The second outcome of the market                                                    |
| **description**  | **str**       | The description of the market                                                       |
| **end_date**     | **str**       | The end date of the market                                                          | [optional] |
| **status**       | **str**       | The status of the market                                                            |
| **tags**         | **List[str]** | The tags of the market                                                              | [optional] |
| **creator_id**   | **str**       | The creator of the market                                                           | [optional] |
| **date_closed**  | **str**       | The date the market was closed                                                      | [optional] |
| **result**       | **str**       | The result of the market. One of None, outcome_1, outcome_2, or void.               | [optional] |
| **image_url**    | **str**       | The URL of the image generated for the market                                       | [optional] |
| **ref_id**       | **str**       | The reference identifier of the market                                              | [optional] |
| **metadata**     | **object**    | Additional metadata for the market. Generally includes order_stat and position_stat | [optional] |

## Example

```python
from kaziro.models.market import Market

# TODO update the JSON string below
json = "{}"
# create an instance of Market from a JSON string
market_instance = Market.from_json(json)
# print the JSON string representation of the object
print(Market.to_json())

# convert the object into a dict
market_dict = market_instance.to_dict()
# create an instance of Market from a dict
market_from_dict = Market.from_dict(market_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
