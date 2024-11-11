import asyncio
import sys
from typing import Optional  # noqa: F401

from ..utils import send_fatal_error
from .agent import Agent

if __name__ == "__main__":
    if len(sys.argv) != 3:
        key = None  # type: Optional[str]
        service = None  # type: Optional[str]
    else:
        key, service = sys.argv[1:]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        agent = Agent(key, service)
        loop.run_until_complete(agent.run())
    except BaseException:
        try:
            send_fatal_error(key, service, "Agent failed.")
        except BaseException:
            pass
        raise
