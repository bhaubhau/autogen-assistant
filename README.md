sudo apt install python3.12-venv  
python3 -m venv ./myenv  
source ./myenv/bin/activate  
pip install pyautogen litellm autogenstudio 'litellm[proxy]' 

litellm --model ollama/tinyllama  

export AUTOGEN_USE_DOCKER=False  
autogenstudio ui  

https://microsoft.github.io/autogen/docs/FAQ/#agents-are-throwing-due-to-docker-not-running-how-can-i-resolve-this  

https://www.youtube.com/watch?v=YqgpGUGBHrU  
https://www.youtube.com/watch?v=rPCdtbA3aLw  

https://microsoft.github.io/autogen/blog/2023/07/14/Local-LLMs/  

python -m fastchat.serve.controller  
python -m fastchat.serve.model_worker --model-path ./downloaded_models/TinyLlama-1.1B-Chat-v1.0 --model-names tinyllama --device cpu  
python -m fastchat.serve.openai_api_server --host localhost --port 8000  