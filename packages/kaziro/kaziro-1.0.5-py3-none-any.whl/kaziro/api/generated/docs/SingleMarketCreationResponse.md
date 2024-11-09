# SingleMarketCreationResponse

## Properties

| Name       | Type                    | Description | Notes      |
| ---------- | ----------------------- | ----------- | ---------- |
| **market** | [**Market**](Market.md) |             |
| **ref_id** | **str**                 |             | [optional] |

## Example

```python
from kaziro.models.single_market_creation_response import SingleMarketCreationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SingleMarketCreationResponse from a JSON string
single_market_creation_response_instance = SingleMarketCreationResponse.from_json(json)
# print the JSON string representation of the object
print(SingleMarketCreationResponse.to_json())

# convert the object into a dict
single_market_creation_response_dict = single_market_creation_response_instance.to_dict()
# create an instance of SingleMarketCreationResponse from a dict
single_market_creation_response_from_dict = SingleMarketCreationResponse.from_dict(single_market_creation_response_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
