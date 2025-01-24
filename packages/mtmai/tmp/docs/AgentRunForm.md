# AgentRunForm


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**form** | [**SchemaForm**](.md) |  | 

## Example

```python
from mtmai.gomtmclients.rest.models.agent_run_form import AgentRunForm

# TODO update the JSON string below
json = "{}"
# create an instance of AgentRunForm from a JSON string
agent_run_form_instance = AgentRunForm.from_json(json)
# print the JSON string representation of the object
print(AgentRunForm.to_json())

# convert the object into a dict
agent_run_form_dict = agent_run_form_instance.to_dict()
# create an instance of AgentRunForm from a dict
agent_run_form_from_dict = AgentRunForm.from_dict(agent_run_form_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


