from pydantic import BaseModel

class TransactionCreate(BaseModel):
    customer_id: int
    product_id: int
    payment_method: str

class TransactionResponse(BaseModel):
    id: int
    customer_id: int
    product_id: int
    amount: float
    payment_method: str
    payment_code: str

    class Config:
        orm_mode: True