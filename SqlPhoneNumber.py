
import re
from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

# Connect to the existing database
engine = create_engine("sqlite:///AccountContacts.db")


# Define the database table
class Base(DeclarativeBase):
    pass


class PhoneContact(Base):
    __tablename__ = "phone_contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str] = mapped_column(
        String(30), nullable=False
    )


# Create the table if it does not exist
Base.metadata.create_all(engine)


def collect_number():
    while True:
        phone_number = input("Please enter your Phone Number: ").strip()

        # Allow digits, spaces, parentheses, and hyphens
        if not re.fullmatch(r"[0-9() -]+", phone_number):
            print("Invalid phone number. Please enter a valid phone number.")
            continue

        # Require at least one digit
        if not any(char.isdigit() for char in phone_number):
            print("Invalid phone number. Please enter a valid phone number.")
            continue

        # Save the phone number to the database
        with Session(engine) as session:
            new_contact = PhoneContact(phone_number=phone_number)
            session.add(new_contact)
            session.commit()

        print(
            f"Thank you! Your phone number '{phone_number}' "
            "has been added to your account."
        )
        return


if __name__ == "__main__":
    collect_number()
