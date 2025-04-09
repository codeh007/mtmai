# AgentProperties


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | 
**provider** | **str** |  | 
**config** | **object** |  | 
**team_id** | **str** |  | 

## Example

```python
from mtmai.clients.rest.models.agent_properties import AgentProperties

# TODO update the JSON string below
json = "{}"
# create an instance of AgentProperties from a JSON string
agent_properties_instance = AgentProperties.from_json(json)
# print the JSON string representation of the object
print(AgentProperties.to_json())

# convert the object into a dict
agent_properties_dict = agent_properties_instance.to_dict()
# create an instance of AgentProperties from a dict
agent_properties_from_dict = AgentProperties.from_dict(agent_properties_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


