from autogen import oai

# create a text completion request
response = oai.Completion.create(
    config_list=[
        {
            "model": "TinyLlama-1.1B-Chat-v1.0",
            "base_url": "http://localhost:8000/v1",
            "api_type": "openai",
            "api_key": "NULL", # just a placeholder
        }
    ],
    prompt="Hi",
)
print(response)

# create a chat completion request
response = oai.ChatCompletion.create(
    config_list=[
        {
            "model": "TinyLlama-1.1B-Chat-v1.0",
            "base_url": "http://localhost:8000/v1",
            "api_type": "openai",
            "api_key": "NULL",
        }
    ],
    messages=[{"role": "user", "content": "Hi"}]
)
print(response)