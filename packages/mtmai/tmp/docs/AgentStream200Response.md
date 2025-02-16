# AgentStream200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | 事件类型 | [optional] 
**quick_start** | [**QuickStart**](QuickStart.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.agent_stream200_response import AgentStream200Response

# TODO update the JSON string below
json = "{}"
# create an instance of AgentStream200Response from a JSON string
agent_stream200_response_instance = AgentStream200Response.from_json(json)
# print the JSON string representation of the object
print(AgentStream200Response.to_json())

# convert the object into a dict
agent_stream200_response_dict = agent_stream200_response_instance.to_dict()
# create an instance of AgentStream200Response from a dict
agent_stream200_response_from_dict = AgentStream200Response.from_dict(agent_stream200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


