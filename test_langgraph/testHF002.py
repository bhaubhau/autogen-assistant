from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline
# model_id = "../downloaded_models/TinyLlama-1.1B-Chat-v1.0"
model_id = "../downloaded_models/gemma-2b-it"
# model_id = "../downloaded_models/Mistral-7B-Instruct-v0.3"
hf = HuggingFacePipeline.from_model_id(
    model_id=model_id,
    task="text-generation",
    pipeline_kwargs=dict(
        max_new_tokens=1024)
)

llm = ChatHuggingFace(llm=hf)
# stop = ["<|system|>","<|user|>","<|assistant|>","</s>"]

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# template = """<|system|>
# you are a helpful assistant</s>
# <|user|>
# {input}</s>
# <|assistant|>"""
# prompt = PromptTemplate.from_template(template)

prompt = ChatPromptTemplate.from_messages([SystemMessage(content="you are a helpful assistant"),
                                           HumanMessage(content="what is the capital of india?"),
                                           AIMessage(content="The capital of india is new delhi")])

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

def chatbot(state: State):
    return {"messages": [llm.invoke(input = state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
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