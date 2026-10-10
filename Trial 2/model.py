from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_engine("sqlite:///contacts.db")


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email_address: Mapped[str | None] = mapped_column(
        String(254), unique=True, nullable=True
    )
    phone_number: Mapped[str | None] = mapped_column(
        String(30), nullable=True
    )


# Create the customers table
Base.metadata.create_all(engine)
