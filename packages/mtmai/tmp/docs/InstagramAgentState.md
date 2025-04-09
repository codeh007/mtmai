# InstagramAgentState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] [default to 'InstagramAgentState']
**version** | **str** |  | [optional] 
**llm_context** | **object** |  | [optional] 
**username** | **str** |  | [optional] 
**password** | **str** |  | [optional] 
**otp_key** | **str** |  | [optional] 
**session_state** | **object** |  | [optional] 
**is_wait_user_input** | **bool** |  | [optional] 
**ig_settings** | **object** |  | [optional] 
**proxy_url** | **str** |  | [optional] 
**platform_account_id** | **str** |  | [optional] 

## Example

```python
from mtmai.clients.rest.models.instagram_agent_state import InstagramAgentState

# TODO update the JSON string below
json = "{}"
# create an instance of InstagramAgentState from a JSON string
instagram_agent_state_instance = InstagramAgentState.from_json(json)
# print the JSON string representation of the object
print(InstagramAgentState.to_json())

# convert the object into a dict
instagram_agent_state_dict = instagram_agent_state_instance.to_dict()
# create an instance of InstagramAgentState from a dict
instagram_agent_state_from_dict = InstagramAgentState.from_dict(instagram_agent_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


