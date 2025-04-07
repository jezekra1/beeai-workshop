import os
from typing import TypedDict

from beeai_sdk.providers.agent import Server
from beeai_sdk.schemas.text import TextInput, TextOutput
from beeai_sdk.schemas.base import Log
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

server = Server("beeai-agents")


def create_graph():
    # Define state
    class State(TypedDict):
        start_point: str
        plan: str

    # Define nodes
    def plan_canal_route(state):
        start = state["start_point"]

        llm = ChatOpenAI(
            model=os.getenv("LLM_MODEL"),
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_API_BASE"),
            temperature=0,
        )
        response = llm.invoke(
            [
                HumanMessage(
                    content=(
                        f"Create a two-hour canal tour starting from {start} in Amsterdam. "
                        f"List 3-4 highlights to see along the way."
                    )
                )
            ]
        )

        state["plan"] = response.content
        return state

    # Build graph
    workflow = StateGraph(State)
    workflow.add_node("plan_canal_route", plan_canal_route)

    # Define edges
    workflow.set_entry_point("plan_canal_route")
    workflow.set_finish_point("plan_canal_route")

    # Compile
    return workflow.compile()


@server.agent()
async def langgraph_agent(input: TextInput) -> TextOutput:
    graph = create_graph()
    async for event in graph.astream(
        {"start_point": input.text}, stream_mode="updates"
    ):
        logs = [
            Log(message=f"🚶‍♂️{key}: {str(value)}", **{key: value})
            for key, value in event.items()
        ]
        output = event
        yield TextOutput(logs=[None, *logs], text="")
    yield TextOutput(text=output["plan_canal_route"]["plan"])


if __name__ == "__main__":
    server()
