# ChatStartInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**tenant_id** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.chat_start_input import ChatStartInput

# TODO update the JSON string below
json = "{}"
# create an instance of ChatStartInput from a JSON string
chat_start_input_instance = ChatStartInput.from_json(json)
# print the JSON string representation of the object
print(ChatStartInput.to_json())

# convert the object into a dict
chat_start_input_dict = chat_start_input_instance.to_dict()
# create an instance of ChatStartInput from a dict
chat_start_input_from_dict = ChatStartInput.from_dict(chat_start_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


