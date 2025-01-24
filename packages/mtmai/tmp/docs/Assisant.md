# Assisant


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**APIResourceMeta**](APIResourceMeta.md) |  | 
**name** | **str** | 助手名称 | [optional] 
**updated_at** | **str** |  | [optional] 
**graph_id** | **str** | 如果后端使用 langgraph ，则返回 langgraph 的 graph_id | [optional] 
**config** | [**AssisantConfig**](AssisantConfig.md) |  | [optional] 
**tags** | **List[str]** |  | 

## Example

```python
from mtmai.gomtmclients.rest.models.assisant import Assisant

# TODO update the JSON string below
json = "{}"
# create an instance of Assisant from a JSON string
assisant_instance = Assisant.from_json(json)
# print the JSON string representation of the object
print(Assisant.to_json())

# convert the object into a dict
assisant_dict = assisant_instance.to_dict()
# create an instance of Assisant from a dict
assisant_from_dict = Assisant.from_dict(assisant_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


