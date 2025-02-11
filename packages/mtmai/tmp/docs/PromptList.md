# PromptList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**PaginationResponse**](PaginationResponse.md) |  | [optional] 
**rows** | [**List[Artifact]**](Artifact.md) |  | [optional] 

## Example

```python
from mtmaisdk.clients.rest.models.prompt_list import PromptList

# TODO update the JSON string below
json = "{}"
# create an instance of PromptList from a JSON string
prompt_list_instance = PromptList.from_json(json)
# print the JSON string representation of the object
print(PromptList.to_json())

# convert the object into a dict
prompt_list_dict = prompt_list_instance.to_dict()
# create an instance of PromptList from a dict
prompt_list_from_dict = PromptList.from_dict(prompt_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


