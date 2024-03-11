from pydantic import BaseModel


class STATUS(BaseModel):
    SOFT_DELETE: str
    ACTIVE: str


Status = STATUS(SOFT_DELETE="SOFT_DELETE", ACTIVE="ACTIVE")
