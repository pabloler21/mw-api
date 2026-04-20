from pydantic import BaseModel, EmailStr


class LeadCreate(BaseModel):
    name: str
    company: str
    email: EmailStr
    destination_port: str | None = None
    product: str
    message: str | None = None


class LeadResponse(BaseModel):
    success: bool
    message: str
