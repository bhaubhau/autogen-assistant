from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.graph import START, END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

@tool
def launch_application(application_name: str):
    """launches the browser and navigate to the application link to be launched

    Args:
        application_name: name of the application to be launched
    """

tools = [launch_application]

tool_node = ToolNode(tools)

# model = ChatOllama(model="llama3.1",temperature=0).bind_tools(tools)
model = ChatOllama(model="mistral:7b-instruct-v0.3-q4_K_M",temperature=0).bind_tools(tools)
# model = ChatOllama(model="mistral-nemo",temperature=0).bind_tools(tools)
# model = ChatOllama(model="mistral-nemo:12b-instruct-2407-q4_K_M",temperature=0).bind_tools(tools)

class State(MessagesState):
    # def __init__(self, page):
    #     super().__init__()
    #     self.page = page
    pass
def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

def chatbot(state: State):
    return {"messages": [model.invoke(state["messages"])]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")

graph_builder.add_conditional_edges("chatbot", should_continue)

graph_builder.add_edge("tools", "chatbot")

graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in graph.stream({"messages": ("user", user_input)}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)