from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'),nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    payment_method: Mapped[str] = mapped_column(nullable=False)
    payment_code: Mapped[str] = mapped_column(nullable=True)

    customer = relationship("Customer", back_populates="transactions")
    product = relationship("Product", back_populates="transactions")