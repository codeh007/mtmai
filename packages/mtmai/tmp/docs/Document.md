# Document

文档

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page_content** | **str** | 页面内容 | 
**metadata** | **object** | 元数据 | 
**score** | **float** | 分数 | 

## Example

```python
from mtmai.gomtmclients.rest.models.document import Document

# TODO update the JSON string below
json = "{}"
# create an instance of Document from a JSON string
document_instance = Document.from_json(json)
# print the JSON string representation of the object
print(Document.to_json())

# convert the object into a dict
document_dict = document_instance.to_dict()
# create an instance of Document from a dict
document_from_dict = Document.from_dict(document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


