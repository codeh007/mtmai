from dotenv import load_dotenv

from mtmaisdk.hatchet import Hatchet

load_dotenv()

hatchet = Hatchet(debug=True)

# client.event.push("user:create", {"test": "test"})
hatchet.event.push(
    "sticky:parent",
    {"test": "test"},
    options={"additional_metadata": {"hello": "moon"}},
)
