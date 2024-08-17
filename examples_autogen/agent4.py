from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

llm_config = {"config_list": [{"model": "tinyllama", "api_key": "NULL", "base_url": "http://localhost:8000/v1"}],
              "seed": 42, "temperature": 0.7}

pros_advocate_prompt = "In charge of arguing for a choice or option. Will follow directions from the debate_moderator and will suggest a pro when asked or will try and rebut an accusation that the option is not to be selected. Only suggest a single pro when prompted, not a list, this allows for fair and even discussion."
pros_advocate = AssistantAgent(
    name="pros_advocate",
    system_message=pros_advocate_prompt,
    llm_config=llm_config,
)

cons_advocate_prompt = "In charge of arguing against a choice or option. Will follow directions from the debate_moderator and will suggest a con when asked or will try and rebut an accusation that the option is to be selected. Only suggest a single con when prompted, not a list, this allows for fair and even discussion."
cons_advocate = AssistantAgent(
    name="cons_advocate",
    system_message=cons_advocate_prompt,
    llm_config=llm_config,
)

debate_moderator_prompt = """
"In charge of facilitating the debate between pros_advocate and cons_advocate. A topic will be given that requires discussion. 

You will start by asking the pros_advocate for an argument why to go with the option, you will then prompt the cons_advocate for a rebuttal. You will then decide if that point stands or not based on the arguments. 
Then you will swap asking for a con from cons_advocate and allowing the pros_advocate a chance to rebut it. 

After 3 pros and cons have been debating declare a final decision to go for or against the proposal and output CONVERSATION_TERMINATE. 

Please note: YOU CANNOT BE ON THE FENCE ABOUT THE DECISION OR OPT OUT OF ANSWERING BY CITING VARIATIONS OF 'it's up to the user'. You must choose either for or against using the provided information."
"""
debate_moderator = AssistantAgent(
    name="debate_moderator",
    system_message=debate_moderator_prompt,
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name="User_Proxy",
    system_message="A human admin.",
    human_input_mode="NEVER", # trust the bots completely, what could go wrong?
    is_termination_msg=lambda x: "CONVERSATION_TERMINATE" in x.get("content", "").rstrip(),
    # code_execution_config=False
    code_execution_config = {"use_docker": False}
)

groupchat = GroupChat(agents=[user_proxy, debate_moderator, pros_advocate, cons_advocate], messages=[], max_round=50)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(manager, message="Should I order takeout tonight?")