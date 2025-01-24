# SubscribeRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**protocol** | **str** | 消息 | [optional] 
**run_id** | **str** | 消息 | [optional] 
**stream_key** | **str** | 消息 | [optional] 
**meta** | **object** | 元数据 | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.subscribe_request import SubscribeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SubscribeRequest from a JSON string
subscribe_request_instance = SubscribeRequest.from_json(json)
# print the JSON string representation of the object
print(SubscribeRequest.to_json())

# convert the object into a dict
subscribe_request_dict = subscribe_request_instance.to_dict()
# create an instance of SubscribeRequest from a dict
subscribe_request_from_dict = SubscribeRequest.from_dict(subscribe_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


