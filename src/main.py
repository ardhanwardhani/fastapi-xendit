from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from src.database import SessionLocal
from src.services.xendit_service import create_payment_va, create_payment_ewallet
from src.models.product import Product
from src.models.customer import Customer
from src.models.transaction import Transaction
from src.schemas.transaction import TransactionCreate, TransactionResponse
from src.models.transaction_new import TransactionNew
from src.schemas.transaction_new import TransactionCreateNew, TransactionNewResponse

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

transactions = []

@app.get("/", response_class=HTMLResponse)
def get_form(request: Request, db: AsyncSession = Depends(get_db)):
    result = db.execute(select(TransactionNew))
    transactions = result.scalars().all()

    return templates.TemplateResponse(
        "form.html", 
        {"request": request, "transactions": transactions}
    )

@app.post("/transaction", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: AsyncSession = Depends(get_db)):
    customer = db.get(Customer, transaction.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    product = db.get(Product, transaction.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    amount = product.price

    try:
        if transaction.payment_method.upper() == "VA":
            payment = create_payment_va(customer.name, amount)
        elif transaction.payment_method.upper() == "EWALLET":
            payment = create_payment_ewallet(amount)
        else:
            raise HTTPException(status_code=400, detail="Invalid payment method")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment creation failed: {str(e)}")
    
    try:
        new_transaction = Transaction(
            customer_id = transaction.customer_id,
            product_id = transaction.product_id,
            amount = amount,
            payment_method = transaction.payment_method,
            payment_code = payment.payment_method.virtual_account.channel_properties.virtual_account_number,
        )
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return {
        "id": new_transaction.id,
        "customer_id": new_transaction.customer_id,
        "product_id": new_transaction.product_id,
        "amount": new_transaction.amount,
        "payment_method": new_transaction.payment_method,
        "payment_code": new_transaction.payment_code
    }

@app.post("/transaction-new", response_class=HTMLResponse)
def create_transaction(
    request: Request,
    customer_name: str = Form(...),
    product_name: str = Form(...),
    amount: float = Form(...),
    payment_method: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        if payment_method.upper() == "VA":
            payment = create_payment_va(customer_name, amount)
        elif payment_method.upper() == "EWALLET":
            payment = create_payment_ewallet(amount)
        else:
            raise HTTPException(status_code=400, detail="Invalid payment method")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment creation failed: {str(e)}")
    
    try:
        new_transaction = TransactionNew(
            customer_name=customer_name,
            product_name=product_name,
            amount=amount,
            payment_method=payment_method,
            payment_code=payment.payment_method.virtual_account.channel_properties.virtual_account_number,
        )
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    result = db.execute(select(TransactionNew))
    transactions = result.scalars().all()

    return templates.TemplateResponse(
        "form.html", 
        {"request": request, "transactions": transactions}
    )