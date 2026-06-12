from fastapi import FastAPI, HTTPException, status
from app.modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from app.modelos.facturas import Factura, FacturaCrear, FacturaEditar
from app.modelos.transacciones import Transaccion,TransaccionCrear, TransaccionEditar


app = FastAPI()

ListaClientes: list[Cliente] = []
ListaFacturas: list[Factura] = []
ListaTransacciones: list[Transaccion] = []
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
async def CrearFactura(cliente_id: int, datos_factura: FacturaCrear):
    #buscar el cliente en la lista clientes
    cliente_encontrado = None
    for cliente in ListaClientes:
        if cliente.id == cliente_id:
           cliente_encontrado = cliente
    # MENSAJE si no existe el cliente
    if not cliente_encontrado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cliente con id {cliente_id} no existe")
    
    #validar datos de la factura
    factura_validada = Factura.model_validate(datos_factura.model_dump())
    factura_validada.cliente = cliente_encontrado
    
    
    #id de la factura
    factura_validada.id = len(ListaFacturas) + 1
    ListaFacturas.append(factura_validada)

    return factura_validada




@app.patch("/facturas/{factura_id}", response_model=Factura)
async def EditarFactura(factura_id: int, datos_factura: Factura):
    pass

@app.delete("/facturas/{factura_id}", response_model=Factura)
async def EliminarFactura(factura_id: int):
    pass





#||||||||||||||||||||||||||||||||
#crear los endpoints para trasacciones

@app.get("/transacciones", response_model=list[Transaccion])
async def ListarTransacciones():
    return ListaTransacciones

@app.get("/transacciones/{transaccion_id}", response_model=Transaccion)
async def ListarTransaccion(transaccion_id: int):
    pass



@app.post("/transacciones/{factura_id}", response_model=Transaccion)
async def CrearTransaccion(factura_id: int, datos_transaccion: TransaccionCrear):
    #buscar una transaccion en la lista transacciones
    transaccion_encontrada = None
    for factura in ListaFacturas:
        if factura.id == factura_id:
           factura_encontrada = factura
    #MENSAJE si no existe la factura
    if not factura_encontrada:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"La Factura con id {factura_id} no existe")
    
    #validar datos de la trasaccion
    transaccion_validada = Transaccion.model_validate(datos_transaccion.model_dump())
    transaccion_validada.factura_id = factura_id
    factura_encontrada.transacciones.append(transaccion_validada)
    
    #id de la trasaccion
    transaccion_validada.id = len(ListaTransacciones) + 1
    return transaccion_validada
    # falto agregar a la lista de transacciones
    ListaTransacciones.append(transaccion_validada)
    return transaccion_validada



@app.patch("/transacciones/{transaccion_id}", response_model=Transaccion)
async def EditarTransaccion(transaccion_id: int, datos_transaccion: Transaccion):
    pass

@app.delete("/transacciones/{transaccion_id}", response_model=Transaccion)
async def EliminarTransaccion(transaccion_id: int):
    pass