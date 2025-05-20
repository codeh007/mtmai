import logging

from hatchet_sdk import ClientTLSConfig, Hatchet
from hatchet_sdk.config import ClientConfig

root_logger = logging.getLogger()

# Initialize Hatchet client
hatchet = Hatchet(
  debug=False,
  config=ClientConfig(
    logger=root_logger,
    # server_url=settings.GOMTM_URL,
    tls_config=ClientTLSConfig(
      #   server_name="app.dev.hatchet-tools.com",
      strategy="none"
    ),
  ),
)
