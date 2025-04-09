# AgentList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[Agent]**](Agent.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.agent_list import AgentList

# TODO update the JSON string below
json = "{}"
# create an instance of AgentList from a JSON string
agent_list_instance = AgentList.from_json(json)
# print the JSON string representation of the object
print(AgentList.to_json())

# convert the object into a dict
agent_list_dict = agent_list_instance.to_dict()
# create an instance of AgentList from a dict
agent_list_from_dict = AgentList.from_dict(agent_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


