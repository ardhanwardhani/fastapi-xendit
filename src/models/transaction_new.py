from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class TransactionNew(Base):
    __tablename__ = "transactions_new"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_name: Mapped[str] = mapped_column(nullable=False)
    product_name: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    payment_method: Mapped[str] = mapped_column(nullable=False)
    payment_code: Mapped[str] = mapped_column(nullable=True)