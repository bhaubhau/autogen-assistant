import os

# from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from huggingface_hub import login
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace

token = os.environ['HUGGINGFACEHUB_API_TOKEN']
login(token)


# llm = ChatOpenAI(base_url="http://localhost:8000/v1", model="tinyllama", api_key="NULL", temperature=0)
# llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-Nemo-Instruct-2407", temperature=0)
# llm = HuggingFaceEndpoint(repo_id="microsoft/Phi-3-mini-4k-instruct", temperature=0)
llm = HuggingFaceEndpoint(repo_id="google/gemma-2b-it", temperature=0)
llm = ChatHuggingFace(llm=llm)

messages = [
    # SystemMessage(content="makemytrip.com is a web application which provides users options to search for train, flights and hotel bookings etc"),
    # SystemMessage(content="As a business analyst you have to write test cases to book flights from mumbai to delhi from make my trip.com"),
    SystemMessage(content="""Below functions are available to perform actions on the site
launch the browser
Enter the dates in the search text box to search for the flights
make the payment for the bookings
select the preferred flight
Select the cities to search for source and destination"""),
    HumanMessage(content="Can you help prepare the scenario with correct steps in order")
]

parser = StrOutputParser()
result = llm.invoke(messages)
print(parser.invoke(result))