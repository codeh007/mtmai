# CreatePostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**site_id** | **str** |  | 
**title** | **str** |  | 
**content** | **str** | The tenant associated with this tenant blog. | 
**slug** | **str** | The slug of the post | 
**author_id** | **str** |  | [optional] 
**status** | **str** |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.create_post_request import CreatePostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreatePostRequest from a JSON string
create_post_request_instance = CreatePostRequest.from_json(json)
# print the JSON string representation of the object
print(CreatePostRequest.to_json())

# convert the object into a dict
create_post_request_dict = create_post_request_instance.to_dict()
# create an instance of CreatePostRequest from a dict
create_post_request_from_dict = CreatePostRequest.from_dict(create_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


