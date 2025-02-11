# SessionRuns


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**runs** | [**List[Run]**](Run.md) |  | 

## Example

```python
from mtmaisdk.clients.rest.models.session_runs import SessionRuns

# TODO update the JSON string below
json = "{}"
# create an instance of SessionRuns from a JSON string
session_runs_instance = SessionRuns.from_json(json)
# print the JSON string representation of the object
print(SessionRuns.to_json())

# convert the object into a dict
session_runs_dict = session_runs_instance.to_dict()
# create an instance of SessionRuns from a dict
session_runs_from_dict = SessionRuns.from_dict(session_runs_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


