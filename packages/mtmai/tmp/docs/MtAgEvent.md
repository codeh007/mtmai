# MtAgEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [default to 'ThoughtEvent']
**source** | **str** |  | 
**content** | **str** |  | 
**metadata** | **object** |  | [optional] 
**models_usage** | **Dict[str, object]** |  | [optional] 
**platform_account_id** | **str** |  | [optional] 
**count_to_follow** | **float** |  | [default to 1]
**username** | **str** |  | 
**password** | **str** |  | 
**otp_key** | **str** |  | [optional] 
**tenant_id** | **str** |  | 
**title** | **str** |  | [optional] 
**task** | **str** |  | 
**config** | [**StartNewChatInputConfig**](StartNewChatInputConfig.md) |  | 

## Example

```python
from mtmai.clients.rest.models.mt_ag_event import MtAgEvent

# TODO update the JSON string below
json = "{}"
# create an instance of MtAgEvent from a JSON string
mt_ag_event_instance = MtAgEvent.from_json(json)
# print the JSON string representation of the object
print(MtAgEvent.to_json())

# convert the object into a dict
mt_ag_event_dict = mt_ag_event_instance.to_dict()
# create an instance of MtAgEvent from a dict
mt_ag_event_from_dict = MtAgEvent.from_dict(mt_ag_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


