sudo apt install python3.12-venv  
python3 -m venv ./myenv  
source ./myenv/bin/activate  
pip install pyautogen litellm autogenstudio 'litellm[proxy]' 

litellm --model ollama/tinyllama
autogenstudio ui



https://www.youtube.com/watch?v=YqgpGUGBHrU  
https://www.youtube.com/watch?v=rPCdtbA3aLw  