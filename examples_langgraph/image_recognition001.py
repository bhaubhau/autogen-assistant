from PIL import Image
import base64
from io import BytesIO
from langchain_ollama import ChatOllama

def convert_to_base64(pil_image: Image):
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def load_image(image_path: str):
    pil_image = Image.open(image_path)
    image_b64 = convert_to_base64(pil_image)
    print("Loaded image successfully!")
    return image_b64

# model = ChatOllama(model="llava-llama3")
model = ChatOllama(model="llava")
# model = ChatOllama(model="llava-phi3:3.8b-mini-fp16")
# model = ChatOllama(model="llava", base_url="http://192.168.0.143:11434")

# image_b64 = load_image("./images/Taj_Mahal.jpeg")
# resp = model.invoke("Which monument from seven wonders of the world from india is present in the image?", images=[image_b64])
# resp = model.invoke("Do you see taj mahal in the image?", images=[image_b64])
# model.bind(images=[image_b64])
# resp = model.invoke("What's in the image?")
# image_b64 = load_image("./images/dogs.jpeg")
# resp = model.invoke("How many kittens are present in the image?", images=[image_b64])
# resp = model.invoke("Are there any dogs present in the image?", images=[image_b64])
image_b64 = load_image("./images/chevy.jpg")
# resp = model.invoke("What's in the image?", images=[image_b64])
model.bind(images=[image_b64])
resp = model.invoke("What's in the image?")
print(resp)