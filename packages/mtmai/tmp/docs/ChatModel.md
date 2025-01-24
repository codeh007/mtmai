# ChatModel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**label** | **str** |  | 
**description** | **str** |  | [optional] 
**icon** | **str** |  | [optional] 
**api_identifier** | **str** |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.chat_model import ChatModel

# TODO update the JSON string below
json = "{}"
# create an instance of ChatModel from a JSON string
chat_model_instance = ChatModel.from_json(json)
# print the JSON string representation of the object
print(ChatModel.to_json())

# convert the object into a dict
chat_model_dict = chat_model_instance.to_dict()
# create an instance of ChatModel from a dict
chat_model_from_dict = ChatModel.from_dict(chat_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


