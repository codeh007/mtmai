# MtLlmMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**content** | [**List[FunctionExecutionResult]**](FunctionExecutionResult.md) |  | 
**source** | **str** |  | [optional] 
**thought** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.mt_llm_message import MtLlmMessage

# TODO update the JSON string below
json = "{}"
# create an instance of MtLlmMessage from a JSON string
mt_llm_message_instance = MtLlmMessage.from_json(json)
# print the JSON string representation of the object
print(MtLlmMessage.to_json())

# convert the object into a dict
mt_llm_message_dict = mt_llm_message_instance.to_dict()
# create an instance of MtLlmMessage from a dict
mt_llm_message_from_dict = MtLlmMessage.from_dict(mt_llm_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


