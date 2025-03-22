# MemoryConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier for the component. | [optional] 
**provider** | **str** | Describes how the component can be instantiated. | 
**component_type** | [**ComponentTypes**](ComponentTypes.md) | Logical type of the component. If missing, the component assumes the default type of the provider. | 
**version** | **int** | Version of the component specification. If missing, the component assumes whatever is the current version of the library used to load it. This is obviously dangerous and should be used for user authored ephmeral config. For all other configs version should be specified. | 
**component_version** | **int** | Version of the component. If missing, the component assumes the default version of the provider. | 
**description** | **str** | Description of the component. | 
**label** | **str** | Human readable label for the component. If missing the component assumes the class name of the provider. | 

## Example

```python
from mtmai.clients.rest.models.memory_config import MemoryConfig

# TODO update the JSON string below
json = "{}"
# create an instance of MemoryConfig from a JSON string
memory_config_instance = MemoryConfig.from_json(json)
# print the JSON string representation of the object
print(MemoryConfig.to_json())

# convert the object into a dict
memory_config_dict = memory_config_instance.to_dict()
# create an instance of MemoryConfig from a dict
memory_config_from_dict = MemoryConfig.from_dict(memory_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


