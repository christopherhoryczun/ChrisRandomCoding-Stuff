#imports
import re

#from data
from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

# Create the database and or connect to the existing database
engine = create_engine("sqlite:///Contacts.db")

# Define the database table
class Base(DeclarativeBase):
    pass

# Account Contact class for email addresses
class AccountContact(Base):
    __tablename__ = "account_contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(
        String(254), unique=True, nullable=False
    )

# Account Contact class for phone numbers
class PhoneContact(Base):
    __tablename__ = "phone_contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str] = mapped_column(
        String(30), nullable=False
    )

# Create the table if it does not exist
Base.metadata.create_all(engine)

# Email collection function
def collect_email():
    valid_extensions = (".com", ".org", ".net", ".edu", ".gov")

    while True:
        email = input("Please enter your email address: ").strip().lower()

        # Check that the email has exactly one @ symbol
        if email.count("@") != 1:
            print("Invalid email. Please enter a valid email address.")
            continue

        # Check the email name and domain
        username, domain = email.split("@")

        if not username or not domain or "." not in domain:
            print("Invalid email address.")
            continue

        # Check the email domain extension
        if not domain.endswith(valid_extensions):
            print(
                "Invalid email domain. Use .com, .org, "
                ".net, .edu, or .gov."
            )
            continue

        # Save the email address to the database
        with Session(engine) as session:
            existing_email = session.query(AccountContact).filter_by(
                email_address=email
            ).first()

            if existing_email:
                print("This email address is already registered.")
                return

            new_contact = AccountContact(email_address=email)
            session.add(new_contact)
            session.commit()

        print(f"Thank you! Your email address '{email}' has been added.")
        return

# Phone number collection function
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

        # Require exactly 10 digits
        digits = [char for char in phone_number if char.isdigit()]
        if len(digits) != 10:
            print(
                f"Invalid phone number. You entered {len(digits)} digits. "
                "Please enter exactly 10 digits."
            )
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

# Main function to run the program
if __name__ == "__main__":
    collect_email()
    collect_number()