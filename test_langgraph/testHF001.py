from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace,HuggingFacePipeline
# from langchain_ollama import ChatOllama
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-Nemo-Instruct-2407", temperature=0)
# llm = HuggingFacePipeline(model_id="../downloaded_models/TinyLlama-1.1B-Chat-v1.0")

model_id = "../downloaded_models/TinyLlama-1.1B-Chat-v1.0"
# model_id = "../downloaded_models/Mistral-7B-Instruct-v0.3"
# tokenizer = AutoTokenizer.from_pretrained(model_id)
# model = AutoModelForCausalLM.from_pretrained(model_id)
# pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=100, device="mps")
# messages = ["""<|system|>
# {{ .System }}</s>
# <|user|>
# {{ .Prompt }}</s>
# <|assistant|>"""
# ]
# pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
# hf = HuggingFacePipeline(pipeline=pipe)
hf = HuggingFacePipeline.from_model_id(
    model_id=model_id,
    task="text-generation",
    # device_map="mps",
    # model_kwargs={"temperature": 0.0, "local_files_only": True},
)
model = ChatHuggingFace(llm=hf)
# model = ChatOllama(model="mistral:7b-instruct-v0.3-q4_K_M")


messages = [
    SystemMessage(content="As an AI assistant respond to user query"),
    HumanMessage(content="what is the capital of india?"),
]

parser = StrOutputParser()
result = model.invoke(messages)
#result = hf.invoke(messages)
print(parser.invoke(result))