# TokenChunk


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | 消息ID | 
**content** | **str** | 消息内容 | 

## Example

```python
from mtmaisdk.clients.rest.models.token_chunk import TokenChunk

# TODO update the JSON string below
json = "{}"
# create an instance of TokenChunk from a JSON string
token_chunk_instance = TokenChunk.from_json(json)
# print the JSON string representation of the object
print(TokenChunk.to_json())

# convert the object into a dict
token_chunk_dict = token_chunk_instance.to_dict()
# create an instance of TokenChunk from a dict
token_chunk_from_dict = TokenChunk.from_dict(token_chunk_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


