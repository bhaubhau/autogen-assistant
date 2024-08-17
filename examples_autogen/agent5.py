from autogen import AssistantAgent, UserProxyAgent
llm_config = {"config_list": [{"model": "tinyllama", "api_key": "NULL", "base_url": "http://localhost:8000/v1"}],
              "seed": 42, "temperature": 0.7}

engineer_agent_prompt = """You are an engineer able to write python code to solve a problem. 
The user will give you a problem to solve and you will need to write code to get the answer. 
The user will run the code and report any problems or errors, you will then create an updated version of your code to address these as they arise. 
If the code executes successfully and returns the needed values output TERMINATE."""
engineer_agent = AssistantAgent(
    name="engineer_agent_prompt",
    system_message=engineer_agent_prompt,
    llm_config=llm_config,
)

executor_user_proxy = UserProxyAgent(
    name="Executor",
    system_message="Executor. Execute the code written by the engineer and report the result.",
    human_input_mode="NEVER",
    code_execution_config={"last_n_messages": 3, "work_dir": "code_dir", "use_docker": False},
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", "").rstrip(),
)

initial_message="""Provided url: https://medium.com/@coldstart_coder/basics-of-the-walrus-operator-in-python-a9b18ca1469c

The provided url is for a medium article. I need you to write a script that will fetch the page, parse the html and print out the title of the article, the author and when it was published. 

I have BeautifulSoup and requests installed so I should be good to go there. 
"""

executor_user_proxy.initiate_chat(engineer_agent, message=initial_message)