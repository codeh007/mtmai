# ChatCompletionsReq


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model** | **str** |  | [optional] 
**messages** | [**List[ChatMessage]**](ChatMessage.md) |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.chat_completions_req import ChatCompletionsReq

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionsReq from a JSON string
chat_completions_req_instance = ChatCompletionsReq.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionsReq.to_json())

# convert the object into a dict
chat_completions_req_dict = chat_completions_req_instance.to_dict()
# create an instance of ChatCompletionsReq from a dict
chat_completions_req_from_dict = ChatCompletionsReq.from_dict(chat_completions_req_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


