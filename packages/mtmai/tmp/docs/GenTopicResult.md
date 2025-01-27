# GenTopicResult

topics 生成结果

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**topics** | **List[str]** | 主题列表，按优先顺序，更好的更靠前 | 

## Example

```python
from mtmaisdk.clients.rest.models.gen_topic_result import GenTopicResult

# TODO update the JSON string below
json = "{}"
# create an instance of GenTopicResult from a JSON string
gen_topic_result_instance = GenTopicResult.from_json(json)
# print the JSON string representation of the object
print(GenTopicResult.to_json())

# convert the object into a dict
gen_topic_result_dict = gen_topic_result_instance.to_dict()
# create an instance of GenTopicResult from a dict
gen_topic_result_from_dict = GenTopicResult.from_dict(gen_topic_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


