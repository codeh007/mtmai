# BlogList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[Blog]**](Blog.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.blog_list import BlogList

# TODO update the JSON string below
json = "{}"
# create an instance of BlogList from a JSON string
blog_list_instance = BlogList.from_json(json)
# print the JSON string representation of the object
print(BlogList.to_json())

# convert the object into a dict
blog_list_dict = blog_list_instance.to_dict()
# create an instance of BlogList from a dict
blog_list_from_dict = BlogList.from_dict(blog_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


