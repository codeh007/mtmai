# MtmaiWorkerConfig200Response

worker 启动时所需的关键配置

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token** | **str** | token | 
**grpc_host_port** | **str** | grpcHostPort | 
**searxng** | **str** | searxng url | [optional] 

## Example

```python
from mtmai.clients.rest.models.mtmai_worker_config200_response import MtmaiWorkerConfig200Response

# TODO update the JSON string below
json = "{}"
# create an instance of MtmaiWorkerConfig200Response from a JSON string
mtmai_worker_config200_response_instance = MtmaiWorkerConfig200Response.from_json(json)
# print the JSON string representation of the object
print(MtmaiWorkerConfig200Response.to_json())

# convert the object into a dict
mtmai_worker_config200_response_dict = mtmai_worker_config200_response_instance.to_dict()
# create an instance of MtmaiWorkerConfig200Response from a dict
mtmai_worker_config200_response_from_dict = MtmaiWorkerConfig200Response.from_dict(mtmai_worker_config200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


