# GenArticleInput

文章生成输入

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**topic** | **str** |  | 

## Example

```python
from mtmai.gomtmclients.rest.models.gen_article_input import GenArticleInput

# TODO update the JSON string below
json = "{}"
# create an instance of GenArticleInput from a JSON string
gen_article_input_instance = GenArticleInput.from_json(json)
# print the JSON string representation of the object
print(GenArticleInput.to_json())

# convert the object into a dict
gen_article_input_dict = gen_article_input_instance.to_dict()
# create an instance of GenArticleInput from a dict
gen_article_input_from_dict = GenArticleInput.from_dict(gen_article_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


