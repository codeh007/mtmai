# PostizChannel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**messages** | [**List[ChatMessage]**](ChatMessage.md) | 聊天消息 | [optional] 
**fresearch** | **str** |  | [optional] 
**org_id** | **str** |  | [optional] 
**hook** | **str** |  | [optional] 
**content** | **str** |  | [optional] 
**var_date** | **str** |  | [optional] 
**category** | **str** |  | [optional] 
**popular_posts** | **str** |  | [optional] 
**topic** | **str** |  | [optional] 
**is_picture** | **bool** |  | [optional] 
**format** | **str** |  | [optional] 
**tone** | **str** |  | [optional] 
**question** | **str** |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.postiz_channel import PostizChannel

# TODO update the JSON string below
json = "{}"
# create an instance of PostizChannel from a JSON string
postiz_channel_instance = PostizChannel.from_json(json)
# print the JSON string representation of the object
print(PostizChannel.to_json())

# convert the object into a dict
postiz_channel_dict = postiz_channel_instance.to_dict()
# create an instance of PostizChannel from a dict
postiz_channel_from_dict = PostizChannel.from_dict(postiz_channel_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


