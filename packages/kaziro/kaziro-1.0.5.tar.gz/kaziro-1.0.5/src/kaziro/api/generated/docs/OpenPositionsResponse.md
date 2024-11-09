# OpenPositionsResponse

## Properties

| Name          | Type                              | Description            | Notes |
| ------------- | --------------------------------- | ---------------------- | ----- |
| **positions** | [**List[Position]**](Position.md) | List of open positions |

## Example

```python
from kaziro.models.open_positions_response import OpenPositionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of OpenPositionsResponse from a JSON string
open_positions_response_instance = OpenPositionsResponse.from_json(json)
# print the JSON string representation of the object
print(OpenPositionsResponse.to_json())

# convert the object into a dict
open_positions_response_dict = open_positions_response_instance.to_dict()
# create an instance of OpenPositionsResponse from a dict
open_positions_response_from_dict = OpenPositionsResponse.from_dict(open_positions_response_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
