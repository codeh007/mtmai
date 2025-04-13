"""Defines constants."""

import os

from mtmai.model_client.utils import get_default_litellm_model

AGENT_NAME = "brand_search_optimization"
DESCRIPTION = "A helpful assistant for brand search optimization."
PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "EMPTY")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
DATASET_ID = os.getenv("DATASET_ID", "products_data_agent")
TABLE_ID = os.getenv("TABLE_ID", "shoe_items")
DISABLE_WEB_DRIVER = int(os.getenv("DISABLE_WEB_DRIVER", 0))
WHL_FILE_NAME = os.getenv("ADK_WHL_FILE", "")
STAGING_BUCKET = os.getenv("STAGING_BUCKET", "")


llm_model = get_default_litellm_model()
MODEL = llm_model
# MODEL = os.getenv("MODEL", "gemini-2.0-flash-001")
