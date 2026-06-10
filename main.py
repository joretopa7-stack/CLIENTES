from fastapi import FastAPI
from modelos.clientes import Cliente, ClienteCrear

app = FastAPI()

ListaClientes: list[Cliente] = []

@app.get("/clientes", response_model=list[Cliente])
def ListarClientes():
    return ListaClientes

@app.get("/clientes/{cliente_id}", response_model=Cliente)
def ListarCliente(cliente_id: int):

    for cliente in ListaClientes:
        if cliente.id == cliente_id:
            return cliente

    return {"error": "Cliente no encontrado"}

@app.post("/clientes", response_model=Cliente)
def AgregarCliente(datos_cliente: ClienteCrear):

    ClienteValidado = Cliente.model_validate(datos_cliente.model_dump())
    
    ListaClientes.append(ClienteValidado)

    return ClienteValidado