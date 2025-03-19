# UpdateBlogRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**description** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.update_blog_request import UpdateBlogRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateBlogRequest from a JSON string
update_blog_request_instance = UpdateBlogRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateBlogRequest.to_json())

# convert the object into a dict
update_blog_request_dict = update_blog_request_instance.to_dict()
# create an instance of UpdateBlogRequest from a dict
update_blog_request_from_dict = UpdateBlogRequest.from_dict(update_blog_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


