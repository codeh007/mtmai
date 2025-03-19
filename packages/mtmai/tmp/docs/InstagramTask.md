# InstagramTask


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_id** | **str** |  | [optional] 
**content** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.instagram_task import InstagramTask

# TODO update the JSON string below
json = "{}"
# create an instance of InstagramTask from a JSON string
instagram_task_instance = InstagramTask.from_json(json)
# print the JSON string representation of the object
print(InstagramTask.to_json())

# convert the object into a dict
instagram_task_dict = instagram_task_instance.to_dict()
# create an instance of InstagramTask from a dict
instagram_task_from_dict = InstagramTask.from_dict(instagram_task_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


