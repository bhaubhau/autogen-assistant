import os

from autogen import ConversableAgent

# agent = ConversableAgent(
#     "chatbot",
#     llm_config={"config_list": [{"model": "gpt-3.5-turbo", "api_key": os.environ.get("OPENAI_API_KEY")}]},
#     code_execution_config=False,  # Turn off code execution, by default it is off.
#     function_map=None,  # No registered functions, by default it is None.
#     human_input_mode="NEVER",  # Never ask for human input.
# )

agent = ConversableAgent(
        "chatbot",
        llm_config={"config_list": [{"model": "tinyllama", "api_key": "NULL", "base_url": "http://localhost:8000/v1"}]},
        code_execution_config=False,  # Turn off code execution, by default it is off.
        function_map=None,  # No registered functions, by default it is None.
        human_input_mode="NEVER",  # Never ask for human input.
    )

reply = agent.generate_reply(messages=[{"content": "can you generate code to book a flight from mumbai to delhi via flipkart.com from chrome ui using playwright python?", "role": "user"}])
print(reply)