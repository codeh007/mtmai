# TextMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**content** | **str** |  | [optional] 
**metadata** | **Dict[str, object]** |  | [optional] 
**models_usage** | **Dict[str, object]** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.text_message import TextMessage

# TODO update the JSON string below
json = "{}"
# create an instance of TextMessage from a JSON string
text_message_instance = TextMessage.from_json(json)
# print the JSON string representation of the object
print(TextMessage.to_json())

# convert the object into a dict
text_message_dict = text_message_instance.to_dict()
# create an instance of TextMessage from a dict
text_message_from_dict = TextMessage.from_dict(text_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


