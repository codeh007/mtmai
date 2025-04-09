# MtOpenAIChatCompletionClientComponent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**provider** | **str** |  | [optional] 
**component_type** | **str** |  | [optional] 
**version** | **int** |  | [optional] 
**component_version** | **int** |  | [optional] 
**description** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**config** | [**OpenAIClientConfigurationConfigModel**](OpenAIClientConfigurationConfigModel.md) |  | 

## Example

```python
from mtmai.clients.rest.models.mt_open_ai_chat_completion_client_component import MtOpenAIChatCompletionClientComponent

# TODO update the JSON string below
json = "{}"
# create an instance of MtOpenAIChatCompletionClientComponent from a JSON string
mt_open_ai_chat_completion_client_component_instance = MtOpenAIChatCompletionClientComponent.from_json(json)
# print the JSON string representation of the object
print(MtOpenAIChatCompletionClientComponent.to_json())

# convert the object into a dict
mt_open_ai_chat_completion_client_component_dict = mt_open_ai_chat_completion_client_component_instance.to_dict()
# create an instance of MtOpenAIChatCompletionClientComponent from a dict
mt_open_ai_chat_completion_client_component_from_dict = MtOpenAIChatCompletionClientComponent.from_dict(mt_open_ai_chat_completion_client_component_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


