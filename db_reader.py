
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

# Import the database models from your existing Python files
from SqlEmail import AccountContact
from SqlPhoneNumber import PhoneContact

# Connect to the existing database
engine = create_engine("sqlite:///Contacts.db")


def read_contacts():
    with Session(engine) as session:

        # Read email addresses
        emails = session.scalars(
            select(AccountContact)
        ).all()

        # Read phone numbers
        phone_numbers = session.scalars(
            select(PhoneContact)
        ).all()

        # Display email addresses
        print("\n===== EMAIL ADDRESSES =====")
        if emails:
            for email in emails:
                print(f"ID: {email.id} | Email: {email.email_address}")
        else:
            print("No email addresses found.")

        # Display phone numbers
        print("\n===== PHONE NUMBERS =====")
        if phone_numbers:
            for phone in phone_numbers:
                print(f"ID: {phone.id} | Phone: {phone.phone_number}")
        else:
            print("No phone numbers found.")


if __name__ == "__main__":
    read_contacts()
