# ChatModelList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[ChatModel]**](ChatModel.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.chat_model_list import ChatModelList

# TODO update the JSON string below
json = "{}"
# create an instance of ChatModelList from a JSON string
chat_model_list_instance = ChatModelList.from_json(json)
# print the JSON string representation of the object
print(ChatModelList.to_json())

# convert the object into a dict
chat_model_list_dict = chat_model_list_instance.to_dict()
# create an instance of ChatModelList from a dict
chat_model_list_from_dict = ChatModelList.from_dict(chat_model_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


