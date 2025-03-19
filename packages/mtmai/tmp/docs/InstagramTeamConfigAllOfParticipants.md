# InstagramTeamConfigAllOfParticipants


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier for the component. | [optional] 
**provider** | **str** |  | 
**component_type** | **str** |  | 
**version** | **int** | Version of the component specification. If missing, the component assumes whatever is the current version of the library used to load it. This is obviously dangerous and should be used for user authored ephmeral config. For all other configs version should be specified. | 
**component_version** | **int** | Version of the component. If missing, the component assumes the default version of the provider. | 
**description** | **str** | Description of the component. | 
**label** | **str** | Human readable label for the component. If missing the component assumes the class name of the provider. | 
**config** | [**AssistantAgentConfig**](AssistantAgentConfig.md) |  | 

## Example

```python
from mtmai.clients.rest.models.instagram_team_config_all_of_participants import InstagramTeamConfigAllOfParticipants

# TODO update the JSON string below
json = "{}"
# create an instance of InstagramTeamConfigAllOfParticipants from a JSON string
instagram_team_config_all_of_participants_instance = InstagramTeamConfigAllOfParticipants.from_json(json)
# print the JSON string representation of the object
print(InstagramTeamConfigAllOfParticipants.to_json())

# convert the object into a dict
instagram_team_config_all_of_participants_dict = instagram_team_config_all_of_participants_instance.to_dict()
# create an instance of InstagramTeamConfigAllOfParticipants from a dict
instagram_team_config_all_of_participants_from_dict = InstagramTeamConfigAllOfParticipants.from_dict(instagram_team_config_all_of_participants_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


