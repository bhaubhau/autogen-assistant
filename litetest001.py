from litellm import completion


messages = [{ "content": "can you write a poem for me","role": "user"}]

# openai call
response = completion(model="ollama/tinyllama", messages=messages)
print(response)