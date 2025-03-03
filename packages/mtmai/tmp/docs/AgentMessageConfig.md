# AgentMessageConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source** | **str** |  | [optional] 
**models_usage** | [**RequestUsage**](RequestUsage.md) |  | [optional] 
**content** | [**List[FunctionExecutionResult]**](FunctionExecutionResult.md) |  | 
**target** | **str** |  | 

## Example

```python
from mtmai.clients.rest.models.agent_message_config import AgentMessageConfig

# TODO update the JSON string below
json = "{}"
# create an instance of AgentMessageConfig from a JSON string
agent_message_config_instance = AgentMessageConfig.from_json(json)
# print the JSON string representation of the object
print(AgentMessageConfig.to_json())

# convert the object into a dict
agent_message_config_dict = agent_message_config_instance.to_dict()
# create an instance of AgentMessageConfig from a dict
agent_message_config_from_dict = AgentMessageConfig.from_dict(agent_message_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


