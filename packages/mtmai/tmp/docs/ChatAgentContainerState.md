# ChatAgentContainerState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**agent_state** | **object** |  | [optional] 
**message_buffer** | [**List[ChatMessage]**](ChatMessage.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.chat_agent_container_state import ChatAgentContainerState

# TODO update the JSON string below
json = "{}"
# create an instance of ChatAgentContainerState from a JSON string
chat_agent_container_state_instance = ChatAgentContainerState.from_json(json)
# print the JSON string representation of the object
print(ChatAgentContainerState.to_json())

# convert the object into a dict
chat_agent_container_state_dict = chat_agent_container_state_instance.to_dict()
# create an instance of ChatAgentContainerState from a dict
chat_agent_container_state_from_dict = ChatAgentContainerState.from_dict(chat_agent_container_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


