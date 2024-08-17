from autogen import AssistantAgent

llm_config = {"config_list": [{"model": "tinyllama", "api_key": "NULL", "base_url": "http://localhost:8000/v1"}],
              "seed": 42, "temperature": 0.7}

pros_cons_agent_instruction_prompt = "This agent will provide a list of pros and cons for a given suggestion. If there is no indication of how many pros and cons make 3 each. If there is no suggestion introduce yourself and prompt for one."

pros_cons_agent = AssistantAgent(
    name="pros_cons_agent",
    system_message=pros_cons_agent_instruction_prompt,
    llm_config=llm_config,
)

topic_suggester_prompt = "You will suggest 3 topics for analysis. You will output each 1 at a time and allow for user feedback for each. Once 3 have been submitted you will then output TERMINATE."
topic_suggester = AssistantAgent(
    name="topic_suggester",
    system_message=topic_suggester_prompt,
    llm_config=llm_config,
)

pros_cons_agent.initiate_chat(topic_suggester,message="Hello! I'm an AI assistant designed to provide a balanced view on any topic by listing pros and cons. Please provide a suggestion or a topic you'd like me to analyze.")
