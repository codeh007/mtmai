# AgentFinish

agent 完成

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**return_values** | **object** | 返回值 | 
**log** | **str** | 日志 | 

## Example

```python
from mtmai.clients.rest.models.agent_finish import AgentFinish

# TODO update the JSON string below
json = "{}"
# create an instance of AgentFinish from a JSON string
agent_finish_instance = AgentFinish.from_json(json)
# print the JSON string representation of the object
print(AgentFinish.to_json())

# convert the object into a dict
agent_finish_dict = agent_finish_instance.to_dict()
# create an instance of AgentFinish from a dict
agent_finish_from_dict = AgentFinish.from_dict(agent_finish_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


