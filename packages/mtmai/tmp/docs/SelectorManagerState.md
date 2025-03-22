# SelectorManagerState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**previous_speaker** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.selector_manager_state import SelectorManagerState

# TODO update the JSON string below
json = "{}"
# create an instance of SelectorManagerState from a JSON string
selector_manager_state_instance = SelectorManagerState.from_json(json)
# print the JSON string representation of the object
print(SelectorManagerState.to_json())

# convert the object into a dict
selector_manager_state_dict = selector_manager_state_instance.to_dict()
# create an instance of SelectorManagerState from a dict
selector_manager_state_from_dict = SelectorManagerState.from_dict(selector_manager_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


