# ScrapeGraphParams


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**input** | **str** |  | [optional] 

## Example

```python
from mtmai.gomtmclients.rest.models.scrape_graph_params import ScrapeGraphParams

# TODO update the JSON string below
json = "{}"
# create an instance of ScrapeGraphParams from a JSON string
scrape_graph_params_instance = ScrapeGraphParams.from_json(json)
# print the JSON string representation of the object
print(ScrapeGraphParams.to_json())

# convert the object into a dict
scrape_graph_params_dict = scrape_graph_params_instance.to_dict()
# create an instance of ScrapeGraphParams from a dict
scrape_graph_params_from_dict = ScrapeGraphParams.from_dict(scrape_graph_params_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


