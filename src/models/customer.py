from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, index=True)

    transactions = relationship("Transaction", back_populates="customer")