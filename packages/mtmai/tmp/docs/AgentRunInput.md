# AgentRunInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | [**FlowNames[str, object]**](.md) |  | [default to FlowNames[str, object].AG]
**is_stream** | **bool** |  | [optional] [default to False]
**params** | [**AgentRunInputParams**](AgentRunInputParams.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput

# TODO update the JSON string below
json = "{}"
# create an instance of AgentRunInput from a JSON string
agent_run_input_instance = AgentRunInput.from_json(json)
# print the JSON string representation of the object
print(AgentRunInput.to_json())

# convert the object into a dict
agent_run_input_dict = agent_run_input_instance.to_dict()
# create an instance of AgentRunInput from a dict
agent_run_input_from_dict = AgentRunInput.from_dict(agent_run_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


