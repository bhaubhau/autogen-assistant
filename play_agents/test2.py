from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(base_url="http://localhost:8000/v1", model="tinyllama", api_key="NULL", temperature=0)

messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="hi how are you?"),
]

parser = StrOutputParser()
result = llm.invoke(messages)
print(parser.invoke(result))