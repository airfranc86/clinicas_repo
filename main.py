from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import csv
import os

app = FastAPI()

# Configuración CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API de Clinicas Repo funcionando correctamente"}

@app.get("/pacientes")
def get_pacientes():
    # Ruta absoluta o relativa al archivo CSV
    csv_path = os.path.join(os.path.dirname(__file__), "datos.csv")
    data = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return JSONResponse(content=data) 
# Aquí puedes agregar futuras rutas para endpoints de datos, reportes, etc. 