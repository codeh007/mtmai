# CrewAiAgent

crawai agent 定义

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | name | 
**role** | **str** | role | 
**backstory** | **str** | role | 
**goal** | **str** | goal | 
**max_retry_limit** | **float** | maxRetryLimit | [optional] 
**max_rpm** | **float** | maxRpm | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.crew_ai_agent import CrewAiAgent

# TODO update the JSON string below
json = "{}"
# create an instance of CrewAiAgent from a JSON string
crew_ai_agent_instance = CrewAiAgent.from_json(json)
# print the JSON string representation of the object
print(CrewAiAgent.to_json())

# convert the object into a dict
crew_ai_agent_dict = crew_ai_agent_instance.to_dict()
# create an instance of CrewAiAgent from a dict
crew_ai_agent_from_dict = CrewAiAgent.from_dict(crew_ai_agent_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


