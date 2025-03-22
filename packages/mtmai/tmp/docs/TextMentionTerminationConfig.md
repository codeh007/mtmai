# TextMentionTerminationConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** |  | 

## Example

```python
from mtmai.clients.rest.models.text_mention_termination_config import TextMentionTerminationConfig

# TODO update the JSON string below
json = "{}"
# create an instance of TextMentionTerminationConfig from a JSON string
text_mention_termination_config_instance = TextMentionTerminationConfig.from_json(json)
# print the JSON string representation of the object
print(TextMentionTerminationConfig.to_json())

# convert the object into a dict
text_mention_termination_config_dict = text_mention_termination_config_instance.to_dict()
# create an instance of TextMentionTerminationConfig from a dict
text_mention_termination_config_from_dict = TextMentionTerminationConfig.from_dict(text_mention_termination_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


