# CustomQuickAction


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | A UUID for the quick action. Used to identify the quick action. | 
**title** | **str** | The title of the quick action. Used in the UI to display the quick action. | 
**prompt** | **str** | The prompt to use when the quick action is invoked. | 
**include_reflections** | **bool** | Whether or not to include the user&#39;s reflections in the prompt. | 
**include_prefix** | **bool** | Whether or not to include the default prefix in the prompt. | 
**include_recent_history** | **bool** | Whether or not to include the last 5 (or less) messages in the prompt. | 

## Example

```python
from mtmaisdk.clients.rest.models.custom_quick_action import CustomQuickAction

# TODO update the JSON string below
json = "{}"
# create an instance of CustomQuickAction from a JSON string
custom_quick_action_instance = CustomQuickAction.from_json(json)
# print the JSON string representation of the object
print(CustomQuickAction.to_json())

# convert the object into a dict
custom_quick_action_dict = custom_quick_action_instance.to_dict()
# create an instance of CustomQuickAction from a dict
custom_quick_action_from_dict = CustomQuickAction.from_dict(custom_quick_action_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


