# TerminationMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reason** | **str** |  | [optional] 
**content** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.termination_message import TerminationMessage

# TODO update the JSON string below
json = "{}"
# create an instance of TerminationMessage from a JSON string
termination_message_instance = TerminationMessage.from_json(json)
# print the JSON string representation of the object
print(TerminationMessage.to_json())

# convert the object into a dict
termination_message_dict = termination_message_instance.to_dict()
# create an instance of TerminationMessage from a dict
termination_message_from_dict = TerminationMessage.from_dict(termination_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


