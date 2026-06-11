from pydantic import BaseModel, computed_field
from .transacciones import Transaccion
from .clientes import Cliente
from datetime import datetime

class FacturaBase(BaseModel):
    fecha: str = datetime.now() 
    cliente: Cliente
    transacciones: list[Transaccion] = []


    @computed_field
    @property
    def vr_total(self) -> float:
        #calcular(cantidad * vr_unitario)
        return 222

class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase):
    id: int | None = None