# CallAgentResult

调用Agent的输出结果

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | **object** |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.call_agent_result import CallAgentResult

# TODO update the JSON string below
json = "{}"
# create an instance of CallAgentResult from a JSON string
call_agent_result_instance = CallAgentResult.from_json(json)
# print the JSON string representation of the object
print(CallAgentResult.to_json())

# convert the object into a dict
call_agent_result_dict = call_agent_result_instance.to_dict()
# create an instance of CallAgentResult from a dict
call_agent_result_from_dict = CallAgentResult.from_dict(call_agent_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


