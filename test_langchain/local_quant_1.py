model_id = "./downloaded_models/Meta-Llama-3.1-8B-Instruct"

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
import torch
from langchain_huggingface import HuggingFacePipeline

tokenizer = AutoTokenizer.from_pretrained(model_id)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

model_trf = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map="auto")
pipe = pipeline("text-generation", model=model_trf, tokenizer=tokenizer, max_new_tokens=1024, device_map="auto")
hf_pipeline = HuggingFacePipeline(pipeline=pipe)

from langchain_core.prompts import PromptTemplate

template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate.from_template(template)

chain = prompt | hf_pipeline

question = "What is electroencephalography?"

print(chain.invoke({"question": question}))