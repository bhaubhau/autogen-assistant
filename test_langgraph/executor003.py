# from pprint import pprint
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

from playwright.async_api import Page


class State(TypedDict):
    # page: Page
    # scenario: str
    messages: Annotated[list, add_messages]

# @tool
# def launch_application(application_name: str):
#     """launches the browser and navigate to the application link to be launched
#
#     Args:
#         application_name: name of the application to be launched
#     """
#     print("Launch tool called for the application:" + application_name)
#
#
# tools = [launch_application]
#
# tool_node = ToolNode(tools)

model = ChatOllama(model="mistral:7b-instruct-v0.3-q4_K_M", temperature=0)
# model.bind_tools(tools)

def should_launch_browser(state: State):
    system_message = SystemMessage(content="""Below applications can be launched for the following actions:
1. makemytrip: For flight bookings, hotel bookings, bus, travel etc
2. flipkart: For purchasing Electronics, apparels, home appliances etc
3. zomato: For ordering food, restaurant reviews
    """)

    last_message=state["messages"][-1]
    print("---------------------------------------------- LaunchBot:--------------------------------------------------")
    response=model.invoke([system_message, HumanMessage(content="User wants to perform the below action:\n" + last_message.content + "\n"
                                                                "Can you tell which application needs to be launched?")])
    print(response.content)
    return {"messages": [AIMessage(content=response.content, user_name="launch_bot")]}


graph_builder = StateGraph(State)
graph_builder.add_node("launch_browser_bot", should_launch_browser)
# graph_builder.add_node("launch_application", launch_application)
graph_builder.add_edge(START, "launch_browser_bot")

graph = graph_builder.compile()

graph.get_graph().print_ascii()

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in graph.stream({"messages": [HumanMessage(content=user_input, user_name="user")]}):
        for value in event.values():
            pass