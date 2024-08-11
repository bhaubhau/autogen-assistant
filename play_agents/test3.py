import langchain
#not working code

model=langchain.load_model("./downloaded_models/TinyLlama-1.1B-Chat-v1.0")

result = model.predict("what is capital of india?")

print(result)