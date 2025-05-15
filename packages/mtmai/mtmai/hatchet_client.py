import logging

from hatchet_sdk import Hatchet
from hatchet_sdk.config import ClientConfig

root_logger = logging.getLogger()

# Initialize Hatchet client
hatchet = Hatchet(
    debug=True,
    config=ClientConfig(
        logger=root_logger,
    ),
)
