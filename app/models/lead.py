from pydantic import BaseModel


class LeadCreate(BaseModel):
    nombre: str
    empresa: str
    email: str
    puerto_destino: str | None = None
    producto: str
    mensaje: str | None = None


class LeadResponse(BaseModel):
    success: bool
    message: str
