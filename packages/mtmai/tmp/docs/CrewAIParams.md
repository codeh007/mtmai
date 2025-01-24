# CrewAIParams


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**input** | **str** |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.crew_ai_params import CrewAIParams

# TODO update the JSON string below
json = "{}"
# create an instance of CrewAIParams from a JSON string
crew_ai_params_instance = CrewAIParams.from_json(json)
# print the JSON string representation of the object
print(CrewAIParams.to_json())

# convert the object into a dict
crew_ai_params_dict = crew_ai_params_instance.to_dict()
# create an instance of CrewAIParams from a dict
crew_ai_params_from_dict = CrewAIParams.from_dict(crew_ai_params_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


