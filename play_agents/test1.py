from autogen import AssistantAgent, UserProxyAgent
from playwright.sync_api import sync_playwright

def launch_application(application):
    with sync_playwright() as p:
        global browser, page
        browser= p.chromium.launch(executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless=False)
        page = browser.new_page()
        if application == "makemytrip":
            page.goto("https://www.makemytrip.com/")
        return "application " + application + " launched successfully"

def login():
    with sync_playwright() as p:
        global page
        page.locator("xpath=//span[@data-cy='closeModal']").click()
        return "logged in successfully"

llm_config = {"config_list": [
                                # {"model": "tinyllama", "api_key": "NULL", "base_url": "http://localhost:8000/v1"},
                                {"model": "gemma", "api_key": "NULL", "base_url": "http://localhost:8000/v1"}
                              ],
              "seed": 10, "temperature": 0.1,
              "functions":[
                  {
                      "name": "launch_application",
                      "description": "user launches the given application",
                      "parameters": {
                          "type": "object",
                          "properties": {
                              "application": {
                                  "type": "string",
                                  "description": "The name of the application to launch"
                              }
                          },
                          "required": ["application"]
                      }
                  },
                  {
                      "name": "login",
                      "description": "user logs in to the application"
                  }
              ]}

test_advisor_prompt = """
"There are users which are testing an application. You are a subject matter expert for the application.
Users testing the application performs some actions and then ask questions about the application.
You will receive the actions performed by the users and suggest them the next steps to take."
"""

test_advisor = AssistantAgent(
    name="test_advisor",
    system_message=test_advisor_prompt,
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
        "launch_application": launch_application,
        "login": login
    }
)

user_proxy.initiate_chat(test_advisor, message="login to makemytrip")