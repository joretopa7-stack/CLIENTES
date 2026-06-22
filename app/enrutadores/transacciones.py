from fastapi import APIRouter, HTTPException, status
from app.modelos.transacciones import Transaccion, TransaccionCrear, TransaccionEditar
from app.modelos.facturas import Factura, FacturaCrear, FacturaEditar
from app.listas import ListaClientes, ListaFacturas, ListaTransacciones

rutas_transacciones = APIRouter()



# 1. Listar todas las transacciones
@rutas_transacciones.get("/transacciones", response_model=list[Transaccion])
async def ListarTransacciones():
    return ListaTransacciones


# 2. Obtener una sola transacción por ID
@rutas_transacciones.get("/transacciones/{transaccion_id}", response_model=Transaccion)
async def ListarTransaccion(transaccion_id: int):
    for transaccion in ListaTransacciones:
        if transaccion.id == transaccion_id:
            return transaccion
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"La transacción con id {transaccion_id} no existe"
    )


# 3. Crear una transacción asociada a una factura 
@rutas_transacciones.post("/facturas/{factura_id}/transacciones", response_model=Transaccion)
async def CrearTransaccion(factura_id: int, datos_transaccion: TransaccionCrear):
    factura_encontrada = None
    
    # Buscar la factura en la lista de facturas
    for factura in ListaFacturas:
        if factura.id == factura_id:
            factura_encontrada = factura
            break 
           
    # Validar si no existe la factura
    if not factura_encontrada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"La Factura con id {factura_id} no existe (Asegúrate de que ya esté creada)"
        )
    
    # Validar datos de la transacción
    transaccion_validada = Transaccion.model_validate(datos_transaccion.model_dump())
    transaccion_validada.factura_id = factura_id
    
    # Generar el id único de la transacción
    transaccion_validada.id = len(ListaTransacciones) + 1
    
    # Asociar al sub-listado interno de la factura
    factura_encontrada.transacciones.append(transaccion_validada)
    
    # Agregar a la lista global de transacciones
    ListaTransacciones.append(transaccion_validada)
    
    return transaccion_validada


# 4. Editar una transacción existente
@rutas_transacciones.patch("/transacciones/{transaccion_id}", response_model=Transaccion)
async def EditarTransaccion(transaccion_id: int, datos_transaccion: TransaccionEditar):
    for i, transaccion in enumerate(ListaTransacciones):
        if transaccion.id == transaccion_id:
            datos_actualizados = transaccion.model_dump()
            campos_nuevos = datos_transaccion.model_dump(exclude_unset=True)
            datos_actualizados.update(campos_nuevos)
            
            transaccion_editada = Transaccion.model_validate(datos_actualizados)
            transaccion_editada.id = transaccion_id
            
            ListaTransacciones[i] = transaccion_editada
            return transaccion_editada

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"La transacción con id {transaccion_id} no existe"
    )


# 5. Eliminar una transacción
@rutas_transacciones.delete("/transacciones/{transaccion_id}", response_model=Transaccion)
async def EliminarTransaccion(transaccion_id: int):
    for i, transaccion in enumerate(ListaTransacciones):
        if transaccion.id == transaccion_id:
            transaccion_eliminada = ListaTransacciones.pop(i)
            
            # Remover la transacción también de la lista interna de su factura
            for factura in ListaFacturas:
                if factura.id == transaccion_eliminada.factura_id:
                    factura.transacciones = [t for t in factura.transacciones if t.id != transaccion_id]
                    break
                    
            return transaccion_eliminada

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"La transacción con id {transaccion_id} no existe"
    )