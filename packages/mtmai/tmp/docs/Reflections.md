# Reflections

生成内容的反思规则

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**style_rules** | **List[str]** | 生成内容时要遵循的样式规则 | 
**content** | **List[str]** | 生成内容时要记住的关于用户的关键内容 | 

## Example

```python
from mtmai.clients.rest.models.reflections import Reflections

# TODO update the JSON string below
json = "{}"
# create an instance of Reflections from a JSON string
reflections_instance = Reflections.from_json(json)
# print the JSON string representation of the object
print(Reflections.to_json())

# convert the object into a dict
reflections_dict = reflections_instance.to_dict()
# create an instance of Reflections from a dict
reflections_from_dict = Reflections.from_dict(reflections_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


