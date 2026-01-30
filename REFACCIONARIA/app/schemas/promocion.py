from pydantic import BaseModel
from typing import Optional

class PromocionBase(BaseModel):
    descripcion: str
    activa: Optional[bool] = True

class PromocionCreate(PromocionBase):
    pass

from pydantic import BaseModel
from typing import Optional

class PromocionUpdate(BaseModel):
    descripcion: Optional[str] = None
    activa: Optional[bool] = None

class PromocionInDBBase(PromocionBase):
    id: int
    class Config:
        orm_mode = True

class Promocion(PromocionInDBBase):
    pass
