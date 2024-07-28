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