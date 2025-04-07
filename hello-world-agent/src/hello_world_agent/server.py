import os

from acp.server.highlevel import Context
from beeai_sdk.providers.agent import Server
from beeai_sdk.schemas.text import TextInput, TextOutput

server = Server("hello-world-agent")

@server.agent()
async def hello_world(input: TextInput, ctx: Context) -> TextOutput:
    """TODO: Your implementation goes here."""
    template = os.getenv("HELLO_TEMPLATE", "Hallo %s")
    return TextOutput(text=template % input.text)
