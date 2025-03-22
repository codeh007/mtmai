# CreateBlogRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | blog title to create. | [optional] 

## Example

```python
from mtmai.clients.rest.models.create_blog_request import CreateBlogRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateBlogRequest from a JSON string
create_blog_request_instance = CreateBlogRequest.from_json(json)
# print the JSON string representation of the object
print(CreateBlogRequest.to_json())

# convert the object into a dict
create_blog_request_dict = create_blog_request_instance.to_dict()
# create an instance of CreateBlogRequest from a dict
create_blog_request_from_dict = CreateBlogRequest.from_dict(create_blog_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


