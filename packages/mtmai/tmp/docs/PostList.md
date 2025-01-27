# PostList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[Post]**](Post.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.post_list import PostList

# TODO update the JSON string below
json = "{}"
# create an instance of PostList from a JSON string
post_list_instance = PostList.from_json(json)
# print the JSON string representation of the object
print(PostList.to_json())

# convert the object into a dict
post_list_dict = post_list_instance.to_dict()
# create an instance of PostList from a dict
post_list_from_dict = PostList.from_dict(post_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


