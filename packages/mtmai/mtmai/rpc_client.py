# import haberdasher_connecpy
import httpx
from mtm.sppb.ag_connecpy import AsyncAgServiceClient

server_url = "http://localhost:3000"
timeout_s = 5


def get_rpc_client(server_url: str, timeout_s: int):
    """
    参考: https://github.com/i2y/connecpy/blob/main/example/async_client.py
    """
    session = httpx.AsyncClient(
        base_url=server_url,
        timeout=timeout_s,
    )
    client = AsyncAgServiceClient(server_url, session=session)

    return client

    # try:
    #     response = await client.MakeHat(
    #         ctx=ClientContext(),
    #         request=haberdasher_pb2.Size(inches=12),
    #         # Optionally provide a session per request
    #         # session=session,
    #         headers={
    #             "Accept-Encoding": "gzip",
    #         },
    #     )
    #     if not response.HasField("name"):
    #         print("We didn't get a name!")
    #     print(response)
    # except ConnecpyServerException as e:
    #     print(e.code, e.message, e.to_dict())
    # finally:
    #     # Close the session (could also use a context manager)
    #     await session.aclose()
