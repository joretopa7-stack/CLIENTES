from pydantic import BaseModel

class TrasaccionBase(BaseModel):
    cantidad: int
    vr_unitario: float
    factura_id: int

class TrasaccionCrear(TrasaccionBase):
    pass

class Trasaccion(TrasaccionBase):
    id: int | None = None