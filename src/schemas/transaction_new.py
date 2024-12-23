from pydantic import BaseModel

class TransactionCreateNew(BaseModel):
    customer_name: str
    product_name: str
    amount: float
    payment_method: str

class TransactionNewResponse(BaseModel):
    id: int
    customer_name: str
    product_name: str
    amount: float
    payment_method: str
    payment_code: str

    class Config:
        orm_mode: True