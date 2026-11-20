
# Read customer contact information from the database.

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from CustomerData import NameContact, AccountContact, PhoneContact

# Connect to the same database
engine = create_engine("sqlite:///CustomerContactInfo.db")


def read_customers():
    with Session(engine) as session:
        customers = session.scalars(
            select(NameContact).order_by(NameContact.customer_id)
        ).all()

        print("\n========== CUSTOMER CONTACTS ==========")

        if not customers:
            print("No customers found.")
            return

        for customer in customers:
            email = session.scalars(
                select(AccountContact).where(
                    AccountContact.customer_id == customer.customer_id
                )
            ).first()

            phone = session.scalars(
                select(PhoneContact).where(
                    PhoneContact.customer_id == customer.customer_id
                )
            ).first()

            print(f"\nCustomer ID: {customer.customer_id}")
            print(f"Name: {customer.full_name}")
            print(
                f"Email: {email.email_address if email else 'Not provided'}"
            )
            print(
                f"Phone: {phone.phone_number if phone else 'Not provided'}"
            )
            print("---------------------------------------")


if __name__ == "__main__":
    read_customers()
