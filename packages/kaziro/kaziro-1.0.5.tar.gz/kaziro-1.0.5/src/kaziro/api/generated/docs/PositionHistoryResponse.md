# PositionHistoryResponse

## Properties

| Name          | Type                              | Description                  | Notes |
| ------------- | --------------------------------- | ---------------------------- | ----- |
| **positions** | [**List[Position]**](Position.md) | List of historical positions |
| **page**      | **int**                           | Current page number          |

## Example

```python
from kaziro.models.position_history_response import PositionHistoryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PositionHistoryResponse from a JSON string
position_history_response_instance = PositionHistoryResponse.from_json(json)
# print the JSON string representation of the object
print(PositionHistoryResponse.to_json())

# convert the object into a dict
position_history_response_dict = position_history_response_instance.to_dict()
# create an instance of PositionHistoryResponse from a dict
position_history_response_from_dict = PositionHistoryResponse.from_dict(position_history_response_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
