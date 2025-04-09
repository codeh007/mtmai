# MyDemoAgentEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [default to 'MyDemoAgentEvent']
**content** | **str** |  | 

## Example

```python
from mtmai.clients.rest.models.my_demo_agent_event import MyDemoAgentEvent

# TODO update the JSON string below
json = "{}"
# create an instance of MyDemoAgentEvent from a JSON string
my_demo_agent_event_instance = MyDemoAgentEvent.from_json(json)
# print the JSON string representation of the object
print(MyDemoAgentEvent.to_json())

# convert the object into a dict
my_demo_agent_event_dict = my_demo_agent_event_instance.to_dict()
# create an instance of MyDemoAgentEvent from a dict
my_demo_agent_event_from_dict = MyDemoAgentEvent.from_dict(my_demo_agent_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


