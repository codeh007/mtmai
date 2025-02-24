import asyncio
import platform


async def run_ag_grpc_host():
    from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost

    host = GrpcWorkerAgentRuntimeHost(address="localhost:7071")
    host.start()  # Start a host service in the background.
    if platform.system() == "Windows":
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            await host.stop()
    else:
        await host.stop_when_signal()
