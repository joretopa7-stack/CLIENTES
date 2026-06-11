from fastapi import FastAPI, HTTPException, status
from modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from modelos.facturas import Factura, FacturaCrear, FacturaEditar
from modelos.transacciones import Transaccion,TrasaccionCrear, TrasaccionEditar


app = FastAPI()

ListaClientes: list[Cliente] = []
ListaFacturas: list[Factura] = []
ListaTrasacciones: list[Transaccion] = []
#endpoint, para obtener o listar todos los clientes

@app.get("/clientes", response_model=list[Cliente])
async def ListarClientes():
    return ListaClientes

#endpoint, para obtener o listar un solo cliente de la lista

@app.get("/clientes/{cliente_id}", response_model=Cliente)
async def ListarCliente(cliente_id: int):
    #recorrer la lista clientes
    for cliente in enumerate(ListaClientes):
        if cliente[1].id == cliente_id:
            return cliente[1]

    raise HTTPException(status_code=404, detail=f"Cliente con id {cliente_id} no encontrado")

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

#endpoint, para eliminar un cliente, y agregar a la lista

@app.delete("/clientes/{cliente_id}", response_model=Cliente)
async def EliminarCliente(cliente_id: int):
    for i, cliente in enumerate(ListaClientes):
        if cliente.id == cliente_id:
            ClienteEliminado = ListaClientes.pop(i)
            return ClienteEliminado

    raise HTTPException(status_code=400, detail=f"El cliente con id {cliente_id} no existe")

#||||||||||||||||||||||||||||||||
#crear los endpoints para facturas

@app.get("/facturas", response_model=list[Factura])
async def ListarFacturas():
    return ListaFacturas

@app.get("/facturas/{factura_id}", response_model=Factura)
async def ListarFactura(factura_id: int):
    #recorrer la lista facturas
    for  factura in enumerate(ListaFacturas):
        if factura[1].id == factura_id:
            return factura[1]

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Factura con id {factura_id} no encontrada")


@app.post("/facturas", response_model=Factura)
async def CrearFactura(cliente_id: int, datos_factura: Factura):
    pass

@app.patch("/facturas/{factura_id}", response_model=Factura)
async def EditarFactura(factura_id: int, datos_factura: Factura):
    pass

@app.delete("/facturas/{factura_id}", response_model=Factura)
async def EliminarFactura(factura_id: int):
    pass

#||||||||||||||||||||||||||||||||
#crear los endpoints para trasacciones

@app.get("/trasacciones", response_model=list[Transaccion])
async def ListarTrasacciones():
    pass

@app.get("/trasacciones/{trasaccion_id}", response_model=Transaccion)
async def ListarTrasaccion(trasaccion_id: int):
    pass

@app.post("/trasacciones/{factura_id}", response_model=Transaccion)
async def CrearTrasaccion(factura_id: int, datos_trasaccion: TrasaccionCrear):
    pass

@app.patch("/trasacciones/{trasaccion_id}", response_model=Transaccion)
async def EditarTrasaccion(trasaccion_id: int, datos_trasaccion: Transaccion):
    pass

@app.delete("/trasacciones/{trasaccion_id}", response_model=Transaccion)
async def EliminarTrasaccion(trasaccion_id: int):
    pass