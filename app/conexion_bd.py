from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine

nombre_bd = "bd_clientes.sqlite3"
url_bd = f"sqlite:///{nombre_bd}"

# Crear el motor de la base de datos
motor_bd = create_engine(url_bd)

#Definir el metodo para crear las tablas 
def crear_tablas(app: FastAPI):
    SQLModel.metadata.create_all(motor_bd)
    yield #no hay nada para retornar o ejecutar 

#Definir metodo para sesiom 

def obtener_session():
    with Session(motor_bd) as mi_session:
        yield mi_session #retorna la sesion para poder usarla en los endpoints

#Denominado inyeccion de dependencias, para poder usar la sesion en los endpoints
#Registrar la sision como dependencia en la aplicacion FastAPI, utilizada en nuestros endpoints 
Sesion_dependencia = Annotated[Session, Depends(obtener_session)]