from pydantic import BaseModel

class ClienteBase(BaseModel):
    nombre: str
    email: str
    descripcion: str

class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass


class Cliente(ClienteBase):
    id: int | None = None