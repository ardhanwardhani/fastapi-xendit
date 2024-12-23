from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False, server_default="0.0")

    transactions = relationship("Transaction", back_populates="product")