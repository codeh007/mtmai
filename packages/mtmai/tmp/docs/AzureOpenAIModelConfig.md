# AzureOpenAIModelConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model** | **str** |  | 
**model_type** | **str** |  | 
**api_key** | **str** |  | [optional] 
**base_url** | **str** |  | [optional] 
**timeout** | **float** |  | [optional] 
**max_retries** | **int** |  | [optional] 
**frequency_penalty** | **float** |  | [optional] 
**logit_bias** | **int** |  | [optional] 
**max_tokens** | **int** |  | [optional] 
**n** | **int** |  | [optional] 
**presence_penalty** | **float** |  | [optional] 
**response_format** | [**ResponseFormat**](ResponseFormat.md) |  | [optional] 
**seed** | **int** |  | [optional] 
**stop** | **List[str]** |  | [optional] 
**temperature** | **float** |  | [optional] 
**top_p** | **float** |  | [optional] 
**user** | **str** |  | [optional] 
**organization** | **str** |  | [optional] 
**default_headers** | **Dict[str, object]** |  | [optional] 
**model_info** | [**ModelInfo**](ModelInfo.md) |  | [optional] 
**azure_deployment** | **str** |  | 
**api_version** | **str** |  | 
**azure_endpoint** | **str** |  | 
**azure_ad_token_provider** | **str** |  | 

## Example

```python
from mtmaisdk.clients.rest.models.azure_open_ai_model_config import AzureOpenAIModelConfig

# TODO update the JSON string below
json = "{}"
# create an instance of AzureOpenAIModelConfig from a JSON string
azure_open_ai_model_config_instance = AzureOpenAIModelConfig.from_json(json)
# print the JSON string representation of the object
print(AzureOpenAIModelConfig.to_json())

# convert the object into a dict
azure_open_ai_model_config_dict = azure_open_ai_model_config_instance.to_dict()
# create an instance of AzureOpenAIModelConfig from a dict
azure_open_ai_model_config_from_dict = AzureOpenAIModelConfig.from_dict(azure_open_ai_model_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


