# from pprint import pprint
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline


class State(TypedDict):
    messages: Annotated[list, add_messages]

# model1 = ChatOllama(model="llama3.1", temperature=0,base_url="http://192.168.0.143:11434") #linux
# model1 = ChatOllama(model="llama3.1", temperature=0,base_url="http://192.168.0.132:9008") #win
# model1 = ChatOllama(model="tinyllama", temperature=0)
model_id = "../downloaded_models/TinyLlama-1.1B-Chat-v1.0"
hf = HuggingFacePipeline.from_model_id(
    model_id=model_id,
    task="text-generation")
model1 = ChatHuggingFace(llm=hf)
model2 = ChatOllama(model="mistral:7b-instruct-v0.3-q4_K_M", temperature=0)

def bot1(state: State):
    # print("I am Bot1:")
    # print("Messages in state:")
    # pprint(state["messages"])
    last_message=state["messages"][-1]
    # if isinstance(last_message, HumanMessage):
    print("--------------------------------------------------Bot1:--------------------------------------------------")
    if last_message.user_name == "user":
        # print("Human message received")
        response=model1.invoke([last_message])
        print(response.content)
        return {"messages": [HumanMessage(content=response.content, user_name="bot1")]}
    else:
        # print("AI message received")
        response=model1.invoke([SystemMessage(content=last_message.content), HumanMessage(content="What are your thoughts about it?")])
        print(response.content)
        return {"messages": [HumanMessage(content=response.content, user_name="bot1")]}

def bot2(state: State):
    # print("I am Bot2:")
    # print("Messages in state:")
    # pprint(state["messages"])
    last_message=state["messages"][-1]
    print("--------------------------------------------------Bot2:--------------------------------------------------")
    response=model2.invoke([SystemMessage(content=last_message.content), HumanMessage(content="What are your thoughts about it?")])
    print(response.content)
    return {"messages": [HumanMessage(content=response.content, user_name="bot2")]}


graph_builder = StateGraph(State)
graph_builder.add_node("bot1", bot1)
graph_builder.add_node("bot2", bot2)
graph_builder.add_edge(START, "bot1")
graph_builder.add_edge("bot1", "bot2")
graph_builder.add_edge("bot2", "bot1")
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