# OHLCData

## Properties

| Name          | Type         | Description | Notes |
| ------------- | ------------ | ----------- | ----- |
| **timestamp** | **datetime** |             |
| **open**      | **float**    |             |
| **high**      | **float**    |             |
| **low**       | **float**    |             |
| **close**     | **float**    |             |
| **volume**    | **float**    |             |

## Example

```python
from kaziro.models.ohlc_data import OHLCData

# TODO update the JSON string below
json = "{}"
# create an instance of OHLCData from a JSON string
ohlc_data_instance = OHLCData.from_json(json)
# print the JSON string representation of the object
print(OHLCData.to_json())

# convert the object into a dict
ohlc_data_dict = ohlc_data_instance.to_dict()
# create an instance of OHLCData from a dict
ohlc_data_from_dict = OHLCData.from_dict(ohlc_data_dict)
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
