# ThoughtEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**source** | **str** |  | 
**content** | **str** |  | [optional] 
**metadata** | **Dict[str, object]** |  | [optional] 
**models_usage** | **Dict[str, object]** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.thought_event import ThoughtEvent

# TODO update the JSON string below
json = "{}"
# create an instance of ThoughtEvent from a JSON string
thought_event_instance = ThoughtEvent.from_json(json)
# print the JSON string representation of the object
print(ThoughtEvent.to_json())

# convert the object into a dict
thought_event_dict = thought_event_instance.to_dict()
# create an instance of ThoughtEvent from a dict
thought_event_from_dict = ThoughtEvent.from_dict(thought_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


