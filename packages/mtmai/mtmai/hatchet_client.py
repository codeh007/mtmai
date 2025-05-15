import logging

from hatchet_sdk import Hatchet
from hatchet_sdk.config import ClientConfig

root_logger = logging.getLogger()
# root_logger.setLevel(logging.INFO)

# Initialize Hatchet client
hatchet = Hatchet(
    debug=True,
    config=ClientConfig(
        logger=root_logger,
    ),
)
