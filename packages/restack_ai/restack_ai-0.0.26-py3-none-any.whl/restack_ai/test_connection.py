import os
import asyncio
from dataclasses import dataclass

from .playground.workflow import playgroundRun
from .restack import Restack

@dataclass
class ConnectionOptions:
    engine_id: str
    address: str
    api_key: str

async def main():
    try:
        # Fetch environment variables
        engine_id = os.environ.get("RESTACK_ENGINE_ID")
        address = os.environ.get("RESTACK_ENGINE_ADDRESS")
        api_key = os.environ.get("RESTACK_ENGINE_API_KEY")

        # Create connection options only if all environment variables are set
        if engine_id and address and api_key:
            connection_options = ConnectionOptions(
                engine_id=engine_id,
                address=address,
                api_key=api_key
            )
            print("connectionOptions", connection_options.model_dump())
            restack = Restack(connection_options)
        else:
            # Instantiate Restack without arguments if environment variables are not set
            restack = Restack()
            print("No environment variables set, using default Restack configuration.")

        print("restackClient", restack)
        await restack.start_service(workflows=[playgroundRun])
        print("Services running successfully.")
    except Exception as e:
        print("Failed to run services", e)

def run_test():
    asyncio.run(main())

if __name__ == "__main__":
    run_test()