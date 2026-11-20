#This is the Personal information needed from every person that is coming to us for work on there car.
#This will include their name, email, phone number, and any other relevant information that we may need to contact them.
#This is only to verify that we have working data.

# Import the tools needed for the database and data validation
import re

#from data
from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

# Connect to the SQLite database
engine = create_engine("sqlite:///CustomerContactInfo.db")

# Base class for all database tables
class Base(DeclarativeBase):
    pass

# Store customer names and generate a unique customer ID
class NameContact(Base):
    __tablename__ = "name_contacts"

    # Unique ID for each customer
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True)

    # Customer's full name
    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False)

# Store customer email addresses
class AccountContact(Base):
    __tablename__ = "account_contacts"

    # Unique ID for each email record
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True)

    # Email address must be unique
    email_address: Mapped[str] = mapped_column(
        String(254),
        unique=True,
        nullable=False)

    # Connect the email to the customer's ID
    customer_id: Mapped[int | None] = mapped_column(
        ForeignKey("name_contacts.id"),
        nullable=True)

#Store customer address information

# Store customer phone numbers
class PhoneContact(Base):
    __tablename__ = "phone_contacts"

    # Unique ID for each phone record
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True)

    # Customer's phone number
    phone_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False)

    # Connect the phone number to the customer's ID
    customer_id: Mapped[int | None] = mapped_column(
        ForeignKey("name_contacts.id"),
        nullable=True)

# Store customer vehicle information

# Create any database tables that do not already exist
Base.metadata.create_all(engine)

# Collect and validate the customer's name
def collect_name():
    while True:
        full_name = input("Enter the customer's full name: ").strip()

        # Make sure the name is not empty
        if not full_name:
            print("Name cannot be empty.")
            continue

        # Allow letters and spaces in the name
        if not all(character.isalpha() or character.isspace()
                   for character in full_name):
            print("Please enter a name using letters and spaces only.")
            continue

        # Return the valid name to the calling program
        return full_name

# Address information will be added in the future. This is a placeholder for now.

# Collect and validate the customer's email address
def collect_email():
    # Accepted email domain endings
    allowed_domains = (".com", ".org", ".net", ".edu", ".gov")

    while True:
        email_address = input("Enter the customer's email address: ").strip()

        # Make sure the email contains exactly one @ symbol
        if email_address.count("@") != 1:
            print("Invalid email. Please use exactly one @ symbol.")
            continue

        # Separate the username and domain
        username, domain = email_address.split("@")

        # Make sure both parts contain information
        if not username or not domain:
            print("Invalid email. Please enter a complete email address.")
            continue

        # Check that the domain ends with an accepted suffix
        if not domain.lower().endswith(allowed_domains):
            print("Email must end in .com, .org, .net, .edu, or .gov.")
            continue

        # Basic check for spaces
        if any(character.isspace() for character in email_address):
            print("Email addresses cannot contain spaces.")
            continue

        # Return the valid email to the calling program
        return email_address

# Collect and validate the customer's phone number
def collect_number():
    while True:
        phone_number = input("Enter the customer's phone number: ").strip()

        # Allow digits, spaces, parentheses, and hyphens
        if not re.fullmatch(r"[0-9 ()-]+", phone_number):
            print("Invalid phone number. Use digits, spaces, parentheses, or hyphens only.")
            continue

        # Remove formatting to check the number of digits
        digits_only = re.sub(r"\D", "", phone_number)

        # Require exactly 10 digits
        if len(digits_only) != 10:
            print("Phone number must contain exactly 10 digits.")
            continue

        # Return the valid phone number to the calling program
        return phone_number

#Vehicle information will be added in the future. This is a placeholder for now.

# Run this section only when CustomerData.py is executed directly. Importing this file from AddCustomer.py will not prompt for information
if __name__ == "__main__":
    print("Customer Data Collection")

    name = collect_name()
    email = collect_email()
    phone = collect_number()

    # Display the collected information without saving it
    print("\nCustomer information collected:")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Phone: {phone}")

    print("\nRun AddCustomer.py to save the customer to the database.")
