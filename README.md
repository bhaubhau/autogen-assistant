sudo apt install python3.12-venv  
python3 -m venv ./myenv  
source ./myenv/bin/activate  
myenv\Scripts\activate  
pip install pyautogen litellm autogenstudio 'litellm[proxy]' 'fschat[model_worker,webui]'  
pip install -U "huggingface_hub[cli]"
pip install --upgrade pip
pip install playwright

litellm --model ollama/tinyllama  

export AUTOGEN_USE_DOCKER=False  
autogenstudio ui  

https://microsoft.github.io/autogen/docs/FAQ/#agents-are-throwing-due-to-docker-not-running-how-can-i-resolve-this  

https://www.youtube.com/watch?v=YqgpGUGBHrU  
https://www.youtube.com/watch?v=rPCdtbA3aLw  

https://microsoft.github.io/autogen/blog/2023/07/14/Local-LLMs/  

python -m fastchat.serve.controller  
python -m fastchat.serve.model_worker --model-path ./downloaded_models/TinyLlama-1.1B-Chat-v1.0 --model-names tinyllama --device cpu
python -m fastchat.serve.model_worker --model-path "C:\Users\Bhavik Kawli\git\autogen-assistant\downloaded_models\TinyLlama-1.1B-Chat-v1.0" --model-names tinyllama --device cpu  
python -m fastchat.serve.model_worker --model-path ./downloaded_models/TinyLlama-1.1B-Chat-v1.0 --model-names tinyllama --device mps --gpus 0,1,2,3 --num-gpus 4  #for apple metal  
python -m fastchat.serve.model_worker --model-path ./downloaded_models/Meta-Llama-3.1-8B-Instruct --model-names llama3.1 --device mps  
python -m fastchat.serve.model_worker --model-path ~/Documents/git/autogen-assistant/downloaded_models/Meta-Llama-3-8B-Instruct --model-names llama3 --device mps --num-gpus 4  
python -m fastchat.serve.model_worker --model-path ~/Documents/git/autogen-assistant/downloaded_models/gemma-7b-it --model-names gemma --device mps --num-gpus 4  
python -m fastchat.serve.model_worker --model-path ~/Documents/git/autogen-assistant/downloaded_models/gemma-2-2b-it --model-names gemma2 --device mps --num-gpus 4  
python -m fastchat.serve.model_worker --model-path ./downloaded_models/gemma-2b-it --model-names gemma --device cpu  
python -m fastchat.serve.multi_model_worker --model-path ~/Documents/git/autogen-assistant/downloaded_models/TinyLlama-1.1B-Chat-v1.0 --model-names tinyllama --model-path ~/Documents/git/autogen-assistant/downloaded_models/gemma-2b-it --model-names gemma --device mps --num-gpus 4  
python -m fastchat.serve.openai_api_server --host localhost --port 8000  


python -m fastchat.serve.gradio_web_server --port 8000  

gnome-session-quit  

https://adithyask.medium.com/from-7b-to-8b-parameters-understanding-weight-matrix-changes-in-llama-transformer-models-31ea7ed5fd88  

https://github.com/meta-llama/llama3  
https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/examples/te_llama/tutorial_accelerate_hf_llama_with_te.html  

ssh bhavik@192.168.0.143  

https://ubuntu.com/server/docs/set-up-an-ftp-server  

huggingface-cli login  
huggingface-cli whoami  
huggingface-cli download meta-llama/Meta-Llama-3.1-8B --local-dir ~/Documents/git/llama3  

scp -r bhavik@192.168.0.143:~/Documents/git/autogen-assistant/downloaded_models downloaded_models  

https://medium.com/@coldstart_coder/conversing-code-unleashing-collaborative-ai-with-the-autogen-framework-a5b04d94b6fd  
https://medium.com/@coldstart_coder/autogen-essentials-function-integration-for-smarter-agents-7c3b4a0fdc12  

https://huggingface.co/spaces/stabilityai/stable-diffusion-3-medium  