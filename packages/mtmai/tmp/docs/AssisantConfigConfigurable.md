# AssisantConfigConfigurable


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**thread_id** | **str** | langgraph 中对应的 threadId | [optional] 
**checkpoint_id** | **str** | langgraph 中对应的 checkpointId | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.assisant_config_configurable import AssisantConfigConfigurable

# TODO update the JSON string below
json = "{}"
# create an instance of AssisantConfigConfigurable from a JSON string
assisant_config_configurable_instance = AssisantConfigConfigurable.from_json(json)
# print the JSON string representation of the object
print(AssisantConfigConfigurable.to_json())

# convert the object into a dict
assisant_config_configurable_dict = assisant_config_configurable_instance.to_dict()
# create an instance of AssisantConfigConfigurable from a dict
assisant_config_configurable_from_dict = AssisantConfigConfigurable.from_dict(assisant_config_configurable_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


