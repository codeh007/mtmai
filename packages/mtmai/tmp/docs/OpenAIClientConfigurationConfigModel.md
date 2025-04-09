# OpenAIClientConfigurationConfigModel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model** | **str** |  | 
**model_type** | [**ModelTypes**](ModelTypes.md) |  | 
**api_key** | **str** |  | [optional] 
**base_url** | **str** |  | [optional] 
**timeout** | **float** |  | [optional] 
**max_retries** | **int** |  | [optional] 
**frequency_penalty** | **float** |  | [optional] 
**logit_bias** | **int** |  | [optional] 
**max_tokens** | **int** |  | [optional] 
**n** | **int** |  | [optional] 
**presence_penalty** | **float** |  | [optional] 
**response_format** | **str** |  | [optional] 
**seed** | **int** |  | [optional] 
**stop** | **List[str]** |  | [optional] 
**temperature** | **float** |  | [optional] 
**top_p** | **float** |  | [optional] 
**user** | **str** |  | [optional] 
**organization** | **str** |  | [optional] 
**default_headers** | **Dict[str, str]** |  | [optional] 
**model_info** | [**ModelInfo**](ModelInfo.md) |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.open_ai_client_configuration_config_model import OpenAIClientConfigurationConfigModel

# TODO update the JSON string below
json = "{}"
# create an instance of OpenAIClientConfigurationConfigModel from a JSON string
open_ai_client_configuration_config_model_instance = OpenAIClientConfigurationConfigModel.from_json(json)
# print the JSON string representation of the object
print(OpenAIClientConfigurationConfigModel.to_json())

# convert the object into a dict
open_ai_client_configuration_config_model_dict = open_ai_client_configuration_config_model_instance.to_dict()
# create an instance of OpenAIClientConfigurationConfigModel from a dict
open_ai_client_configuration_config_model_from_dict = OpenAIClientConfigurationConfigModel.from_dict(open_ai_client_configuration_config_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


