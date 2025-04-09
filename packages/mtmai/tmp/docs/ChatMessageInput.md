# ChatMessageInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [default to 'ChatMessageInput']
**content** | **str** |  | 

## Example

```python
from mtmai.clients.rest.models.chat_message_input import ChatMessageInput

# TODO update the JSON string below
json = "{}"
# create an instance of ChatMessageInput from a JSON string
chat_message_input_instance = ChatMessageInput.from_json(json)
# print the JSON string representation of the object
print(ChatMessageInput.to_json())

# convert the object into a dict
chat_message_input_dict = chat_message_input_instance.to_dict()
# create an instance of ChatMessageInput from a dict
chat_message_input_from_dict = ChatMessageInput.from_dict(chat_message_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


