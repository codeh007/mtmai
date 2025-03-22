# AgentRunInputOther


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**cookies** | **str** |  | [optional] 
**session** | **str** |  | [optional] 
**email** | **str** |  | [optional] 
**password** | **str** |  | [optional] 
**username** | **str** |  | [optional] 
**api_token** | **str** |  | [optional] 
**resource_id** | **str** |  | [optional] 
**content** | **str** |  | 
**thread_id** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**reason** | **str** |  | [optional] 
**session_id** | **str** |  | 
**code_writing_task** | **str** |  | 
**code_writing_scratchpad** | **str** |  | 
**code** | **str** |  | 
**review** | **str** |  | 
**approved** | **bool** |  | 
**url** | **str** |  | 
**messages** | **List[Dict[str, object]]** |  | 
**stop_reason** | **str** |  | 

## Example

```python
from mtmai.clients.rest.models.agent_run_input_other import AgentRunInputOther

# TODO update the JSON string below
json = "{}"
# create an instance of AgentRunInputOther from a JSON string
agent_run_input_other_instance = AgentRunInputOther.from_json(json)
# print the JSON string representation of the object
print(AgentRunInputOther.to_json())

# convert the object into a dict
agent_run_input_other_dict = agent_run_input_other_instance.to_dict()
# create an instance of AgentRunInputOther from a dict
agent_run_input_other_from_dict = AgentRunInputOther.from_dict(agent_run_input_other_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


