
# Import the database session and customer models
from sqlalchemy.orm import Session

from CustomerData import (
    engine,
    NameContact,
    AccountContact,
    PhoneContact,
    collect_name,
    collect_email,
    collect_number
)


# Add a new customer to the database
def add_customer():
    print("===== Add New Customer =====")

    # Collect and validate the customer's information
    name = collect_name()
    email = collect_email()
    phone = collect_number()

    # Open a database session
    with Session(engine) as session:
        try:
            # Create the customer record first
            customer = NameContact(full_name=name)
            session.add(customer)

            # Generate the customer ID before adding related records
            session.flush()

            # Save the customer's email with the same customer ID
            email_contact = AccountContact(
                email_address=email,
                customer_id=customer.id
            )
            session.add(email_contact)

            # Save the customer's phone with the same customer ID
            phone_contact = PhoneContact(
                phone_number=phone,
                customer_id=customer.id
            )
            session.add(phone_contact)

            # Commit all three records together
            session.commit()

            # Display the result
            print("\nCustomer added successfully!")
            print(f"Customer ID: {customer.id}")
            print(f"Name: {name}")
            print(f"Email: {email}")
            print(f"Phone: {phone}")

        except Exception as error:
            # Undo incomplete changes if something goes wrong
            session.rollback()
            print("\nUnable to add customer.")
            print(f"Error: {error}")


# Start the program when this file is run directly
if __name__ == "__main__":
    add_customer()
