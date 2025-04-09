# BaseGroupChatManagerState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**message_thread** | **List[object]** |  | [optional] 
**current_turn** | **int** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.base_group_chat_manager_state import BaseGroupChatManagerState

# TODO update the JSON string below
json = "{}"
# create an instance of BaseGroupChatManagerState from a JSON string
base_group_chat_manager_state_instance = BaseGroupChatManagerState.from_json(json)
# print the JSON string representation of the object
print(BaseGroupChatManagerState.to_json())

# convert the object into a dict
base_group_chat_manager_state_dict = base_group_chat_manager_state_instance.to_dict()
# create an instance of BaseGroupChatManagerState from a dict
base_group_chat_manager_state_from_dict = BaseGroupChatManagerState.from_dict(base_group_chat_manager_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


