import os
from pprint import pprint
from typing import Annotated, Literal, TypedDict
from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from huggingface_hub import login


token = os.environ['HUGGINGFACEHUB_API_TOKEN']
login(token)


# Define the tools for the agent to use
@tool
def launch_browser(url: str):
    pprint("url to launch is: " + url)
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


tools = [launch_browser]

tool_node = ToolNode(tools)



# model = ChatOpenAI(model="tinyllama", api_key="NULL", base_url="http://localhost:8000/v1", temperature=0).bind_tools(tools)
# llm = HuggingFaceEndpoint(repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0", temperature=0)
# llm = HuggingFaceEndpoint(repo_id="google/gemma-2b-it", temperature=0)
# model = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0).bind_tools(tools)
llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-Nemo-Instruct-2407", temperature=0)
# llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.3", temperature=0)
# llm = HuggingFaceEndpoint(repo_id="microsoft/Phi-3-mini-4k-instruct", temperature=0)
model = ChatHuggingFace(llm=llm).bind_tools(tools)

# Define the function that determines whether to continue or not
def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        # if "real-time weather data" in last_message.content:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return END


# Define the function that calls the model
def call_model(state: MessagesState):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}


# Define a new graph
workflow = StateGraph(MessagesState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.set_entry_point("agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
    # {"tools": "tools", "__end__": "__end__"}
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("tools", 'agent')

# Initialize memory to persist state between graph runs
checkpointer = MemorySaver()

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable.
# Note that we're (optionally) passing the memory when compiling the graph
app = workflow.compile(checkpointer=checkpointer)

import json
with open('test7_funcs.json') as f:
    tools_description = json.load(f)

# Use the Runnable
final_state = app.invoke(
    {"messages": [
        SystemMessage(content="You are a helpful assistant with access to the following functions. Use them if required -\n" + str(tools_description)),
        # HumanMessage(content="what is the weather in sf"),
        HumanMessage(content="can you launch the link huggingface.co"),
    ]},
    config={"configurable": {"thread_id": 42}}
)
print(final_state["messages"][-1].content)

final_state = app.invoke(
    {"messages": [HumanMessage(content="what about ny")]},
    config={"configurable": {"thread_id": 42}}
)
print(final_state["messages"][-1].content)