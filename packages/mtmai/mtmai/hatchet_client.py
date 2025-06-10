from hatchet_sdk import Hatchet
from hatchet_sdk.config import ClientConfig

hatchet = Hatchet(
  debug=False,
  config=ClientConfig(
    # token="eyJhbGciOiJFUzI1NiIsICJraWQiOiJjZFFwTkEifQ.eyJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjgzODMiLCAiZXhwIjo0OTAzMDY2MjA1LCAiZ3JwY19icm9hZGNhc3RfYWRkcmVzcyI6IjEyNy4wLjAuMTo3MDcwIiwgImlhdCI6MTc0OTQ2NjIwNSwgImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODM4MyIsICJzZXJ2ZXJfdXJsIjoiaHR0cDovL2xvY2FsaG9zdDo4MzgzIiwgInN1YiI6IjcwN2QwODU1LTgwYWItNGUxZi1hMTU2LWYxYzQ1NDZjYmY1MiIsICJ0b2tlbl9pZCI6Ijk2NDg0OGNhLTBkODItNGUwNy05MGZlLWFiMmJkMWJmNmM5NCJ9.vomg8r-v7cvHDWxX54nm9xFqlyhV4kTJTvHbyVkRreA-hvDISw4N1ky_SGlGKXJ7cVyxTF3mLVzSqqvbqKgn7g",
    # logger=root_logger,
    # server_url=settings.GOMTM_URL,
    # tls_config=ClientTLSConfig(
    #   #   server_name="app.dev.hatchet-tools.com",
    #   strategy="none"
    # ),
  ),
)
