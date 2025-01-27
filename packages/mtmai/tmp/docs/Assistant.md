# Assistant


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assistant_id** | **str** | The ID of the assistant | 
**graph_id** | **str** | The ID of the graph | 
**config** | **object** | The assistant config | 
**created_at** | **str** | The time the assistant was created | 
**metadata** | **object** | The assistant metadata | 
**version** | **float** | The version of the assistant | 
**updated_at** | **str** | The last time the assistant was updated | 
**name** | **str** | The name of the assistant | 

## Example

```python
from mtmaisdk.clients.rest.models.assistant import Assistant

# TODO update the JSON string below
json = "{}"
# create an instance of Assistant from a JSON string
assistant_instance = Assistant.from_json(json)
# print the JSON string representation of the object
print(Assistant.to_json())

# convert the object into a dict
assistant_dict = assistant_instance.to_dict()
# create an instance of Assistant from a dict
assistant_from_dict = Assistant.from_dict(assistant_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


