from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import process

app = FastAPI()

# Configura los orígenes permitidos
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:5500",
    # Agrega aquí cualquier otro origen permitido
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite los orígenes especificados
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/process_image")
async def process_image(image_path):
    # descarga la imagen
    with open("./temp/image_recibida.jpg", "wb") as image:
        image.write(requests.get(image_path).content)
    # procesa la imagen
    image_path = "./temp/image_recibida.jpg"
    res = process.autoDetect(image_path)
    # Movemos las imagenes temp y temp3 a la carpeta web\public\images-processed
    with open("./web/public/images-processed/temp.jpg", "wb") as image:
        image.write(open("temp.jpg", "rb").read())
    with open("./web/public/images-processed/temp3.jpg", "wb") as image:
        image.write(open("temp3.jpg", "rb").read())

    return res