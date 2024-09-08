from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace,HuggingFacePipeline
# from langchain_ollama import ChatOllama

# llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-Nemo-Instruct-2407", temperature=0)
llm = HuggingFacePipeline(model_id="../downloaded_models/TinyLlama-1.1B-Chat-v1.0")
model = ChatHuggingFace(llm=llm)
# model = ChatOllama(model="mistral:7b-instruct-v0.3-q4_K_M")


messages = [
    SystemMessage(content="As an AI assistant respond to user query"),
    HumanMessage(content="where is india?"),
]

parser = StrOutputParser()
result = model.invoke(messages)
print(parser.invoke(result))