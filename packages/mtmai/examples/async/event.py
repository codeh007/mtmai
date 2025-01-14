from dotenv import load_dotenv

from mtmaisdk import Hatchet

load_dotenv()

hatchet = Hatchet()
hatchet.event.push("async:create", {"test": "test"})
