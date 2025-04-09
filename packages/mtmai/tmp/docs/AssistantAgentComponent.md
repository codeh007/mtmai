# AssistantAgentComponent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**provider** | **str** |  | [optional] 
**component_type** | **str** |  | [default to 'agent']
**version** | **int** |  | [optional] 
**component_version** | **int** |  | [optional] 
**description** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**config** | [**AssistantAgentConfig**](AssistantAgentConfig.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.assistant_agent_component import AssistantAgentComponent

# TODO update the JSON string below
json = "{}"
# create an instance of AssistantAgentComponent from a JSON string
assistant_agent_component_instance = AssistantAgentComponent.from_json(json)
# print the JSON string representation of the object
print(AssistantAgentComponent.to_json())

# convert the object into a dict
assistant_agent_component_dict = assistant_agent_component_instance.to_dict()
# create an instance of AssistantAgentComponent from a dict
assistant_agent_component_from_dict = AssistantAgentComponent.from_dict(assistant_agent_component_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


