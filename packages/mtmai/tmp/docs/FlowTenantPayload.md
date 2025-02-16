# FlowTenantPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**input** | **str** | 输入 | [optional] 

## Example

```python
from mtmai.clients.rest.models.flow_tenant_payload import FlowTenantPayload

# TODO update the JSON string below
json = "{}"
# create an instance of FlowTenantPayload from a JSON string
flow_tenant_payload_instance = FlowTenantPayload.from_json(json)
# print the JSON string representation of the object
print(FlowTenantPayload.to_json())

# convert the object into a dict
flow_tenant_payload_dict = flow_tenant_payload_instance.to_dict()
# create an instance of FlowTenantPayload from a dict
flow_tenant_payload_from_dict = FlowTenantPayload.from_dict(flow_tenant_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


