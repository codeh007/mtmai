# ChatWelcome


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | 欢迎语标题 | [optional] 
**content** | **str** | 欢迎语内容 | [optional] 
**sub_title** | **str** | 主标题 | [optional] 
**quick_starts** | [**List[QuickStart]**](QuickStart.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.chat_welcome import ChatWelcome

# TODO update the JSON string below
json = "{}"
# create an instance of ChatWelcome from a JSON string
chat_welcome_instance = ChatWelcome.from_json(json)
# print the JSON string representation of the object
print(ChatWelcome.to_json())

# convert the object into a dict
chat_welcome_dict = chat_welcome_instance.to_dict()
# create an instance of ChatWelcome from a dict
chat_welcome_from_dict = ChatWelcome.from_dict(chat_welcome_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


