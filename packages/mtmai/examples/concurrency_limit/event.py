from dotenv import load_dotenv

from mtmaisdk import new_client

load_dotenv()

client = new_client()

client.event.push("concurrency-test", {"group": "test"})
