from autogen import AssistantAgent, UserProxyAgent

llm_config={"config_list": [{"model": "tinyllama", "api_key": "NULL", "base_url": "http://localhost:8000/v1"}], "seed": 42, "temperature": 0.7}

pros_cons_agent_instruction_prompt = "This agent will provide a list of pros and cons for a given suggestion. If there is no indication of how many pros and cons make 3 each. If there is no suggestion introduce yourself and prompt for one."

pros_cons_agent = AssistantAgent(
        name="pros_cons_agent",
        system_message=pros_cons_agent_instruction_prompt,
        llm_config=llm_config,
)

user_proxy = UserProxyAgent(
        name="User_Proxy",
        system_message="A human admin.",
        human_input_mode="ALWAYS"
)

pros_cons_agent.initiate_chat(user_proxy, message="Hello! I'm an AI assistant designed to provide a balanced view on any topic by listing pros and cons. Please provide a suggestion or a topic you'd like me to analyze.")