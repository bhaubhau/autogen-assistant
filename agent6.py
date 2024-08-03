from autogen import AssistantAgent, UserProxyAgent


name_to_account_id = {
    "Alice": "A123",
    "Bob": "B456",
    "Charlie": "C789"
}

account_id_to_bill = {
    "A123": 120.50,
    "B456": 200.75,
    "C789": 99.99
}

def get_account_id(name):
    return name_to_account_id.get(name, "Name not found")

def get_last_bill_amount(account_id):
    return account_id_to_bill.get(account_id, "Account ID not found")


llm_config = {"config_list": [{"model": "tinyllama", "api_key": "NULL", "base_url": "http://localhost:8000/v1"}],
              "seed": 42, "temperature": 0.0,
              "functions":[
                  {
                      "name": "get_account_id",
                      "description": "retrieves the account id for a user given their name",
                      "parameters": {
                          "type": "object",
                          "properties": {
                              "name":{
                                  "type": "string",
                                  "description": "The name of the customer that will be used to lookup the account id"
                              }
                          },
                          "required": ["name"]
                      }
                  },
                  {
                      "name": "get_last_bill_amount",
                      "description": "Retrieves the last bill amount for a user for a given account id.",
                      "parameters": {
                          "type": "object",
                          "properties": {
                              "account_id":{
                                  "type": "string",
                                  "description": "The account id fetched from get_account_id that will be used to lookup the last bill for the customer"
                              }
                          },
                          "required": ["account_id"]
                      }
                  }
              ]
            }

billing_assistant_agent_prompt = '''
This agent is a helpful assistant that can retrieve the account id and the last bill amount for a customer. 
Any other customer care requests are outside the scope of this agent. 
Once you have completed assisting the user output TERMINATE'''
# create the agent and give it the config with our function definitions defined
billing_assistant_agent = AssistantAgent(
    name="billing_assistant_agent",
    system_message=billing_assistant_agent_prompt,
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config = {"use_docker": False}
)

user_proxy.register_function(
    function_map={
        "get_account_id": get_account_id,
        "get_last_bill_amount": get_last_bill_amount,
    }
)

user_proxy.initiate_chat(billing_assistant_agent, message="My name is Bob, can you tell me what my last bill was?")