from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama

class State(TypedDict):
    messages: Annotated[list, add_messages]

model1 = ChatOllama(model="llama3.1", temperature=0)
model2 = ChatOllama(model="tinyllama", temperature=0)
model3 = ChatOllama(model="mistral:7b-instruct-v0.3-q4_K_M", temperature=0)
model4 = ChatOllama(model="gemma2:2b", temperature=0)

def bot1(state: State):
    return {"messages": [model1.invoke(state["messages"])]}

def bot2(state: State):
    return {"messages": [model2.invoke(state["messages"])]}

def bot3(state: State):
    return {"messages": [model3.invoke(state["messages"])]}

def bot4(state: State):
    return {"messages": [model4.invoke(state["messages"])]}

graph_builder = StateGraph(State)
graph_builder.add_node("bot1", bot1)
graph_builder.add_node("bot2", bot2)
graph_builder.add_node("bot3", bot3)
graph_builder.add_node("bot4", bot3)
graph_builder.add_edge(START, "bot1")
graph_builder.add_edge("bot1", "bot2")
graph_builder.add_edge("bot2", "bot3")
graph_builder.add_edge("bot3", "bot4")
graph_builder.add_edge("bot4", "bot1")
graph = graph_builder.compile()

graph.get_graph().print_ascii()

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in graph.stream({"messages": ("user", user_input)}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)