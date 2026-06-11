from pydantic import BaseModel
from .clientes import Cliente

class FacturaBase(BaseModel):
    fecha: str
    vr_total: float
    cliente: Cliente

class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase):
    id: int | None = None