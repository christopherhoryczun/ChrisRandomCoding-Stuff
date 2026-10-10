```python
# Import the database session and customer models
from sqlalchemy import select
from sqlalchemy.orm import Session

from CustomerData import (
    engine,
    NameContact,
    AccountContact,
    PhoneContact
)


# List all customers stored in the database
def list_customers():
    print("===== Customer List =====")

    # Open a connection to the database
    with Session(engine) as session:

        # Get all customer records
        customers = session.scalars(
            select(NameContact).order_by(NameContact.id)
        ).all()

        # Check whether the database contains any customers
        if not customers:
            print("No customers found in the database.")
            return

        # Display each customer's information
        for customer in customers:

            # Find the customer's email addresses
            emails = session.scalars(
                select(AccountContact.email_address).where(
                    AccountContact.customer_id == customer.id
                )
            ).all()

            # Find the customer's phone numbers
            phone_numbers = session.scalars(
                select(PhoneContact.phone_number).where(
                    PhoneContact.customer_id == customer.id
                )
            ).all()

            # Display the customer's details
            print("-----------------------------------")
            print(f"Customer ID: {customer.id}")
            print(f"Name: {customer.full_name}")
            print(
                "Email: "
                + (", ".join(emails) if emails else "Not available")
            )
            print(
                "Phone: "
                + (
                    ", ".join(phone_numbers)
                    if phone_numbers
                    else "Not available"
                )
            )

        print("-----------------------------------")
        print(f"Total customers: {len(customers)}")


# Run the program when this file is executed directly
if __name__ == "__main__":
    list_customers()
```
