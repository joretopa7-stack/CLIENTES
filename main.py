from fastapi import FastAPI, HTTPException
from modelos.clientes import Cliente, ClienteCrear, ClienteEditar

app = FastAPI()

ListaClientes: list[Cliente] = []

#endpoint, para obtener o listar todos los clientes

@app.get("/clientes", response_model=list[Cliente])
async def ListarClientes():
    return ListaClientes

#endpoint, para obtener o listar un solo cliente de la lista

@app.get("/clientes/{cliente_id}", response_model=Cliente)
async def ListarCliente(cliente_id: int):
    #recorrer la lista clientes
    for i, cliente in enumerate(ListaClientes):
        if cliente[i].id == cliente_id:
            return cliente[i]

    raise HTTPException(status_code=404, detail="Cliente no encontrado")

#endpoint, para crear un cliente, y agregar a la lista

@app.post("/clientes", response_model=Cliente)
async def AgregarCliente(datos_cliente: ClienteCrear):

    ClienteValidado = Cliente.model_validate(datos_cliente.model_dump())
    
    #generar id
    id_cliente = len(ListaClientes) + 1
    ClienteValidado.id = id_cliente
    ListaClientes.append(ClienteValidado)

    return ClienteValidado


#endpoint, para editar un cliente, y agregar a la lista

@app.patch("/clientes/{cliente_id}", response_model=Cliente)
async def EditarCliente(cliente_id: int, datos_cliente: ClienteEditar):
    for i, cliente in enumerate(ListaClientes):
        if cliente.id == cliente_id:
            #validar los datos del cliente
            ClienteValidado = Cliente.model_validate(datos_cliente.model_dump())
            ClienteValidado.id = cliente_id
            ListaClientes[i] = ClienteValidado
            return ClienteValidado

    raise HTTPException(status_code=400, detail=f"El cliente con id {cliente_id} no existe")

    