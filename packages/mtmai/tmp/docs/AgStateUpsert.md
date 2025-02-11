# AgStateUpsert


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | **str** |  | [default to '1.0.0']
**type** | **str** |  | [optional] [default to 'TeamState']
**state** | **Dict[str, object]** |  | 

## Example

```python
from mtmaisdk.clients.rest.models.ag_state_upsert import AgStateUpsert

# TODO update the JSON string below
json = "{}"
# create an instance of AgStateUpsert from a JSON string
ag_state_upsert_instance = AgStateUpsert.from_json(json)
# print the JSON string representation of the object
print(AgStateUpsert.to_json())

# convert the object into a dict
ag_state_upsert_dict = ag_state_upsert_instance.to_dict()
# create an instance of AgStateUpsert from a dict
ag_state_upsert_from_dict = AgStateUpsert.from_dict(ag_state_upsert_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


