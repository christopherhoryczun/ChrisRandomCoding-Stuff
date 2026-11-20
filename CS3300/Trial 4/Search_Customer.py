#This is to see what I need to do to get the search function to work. I will be using the list customer function as a base for this.

#imports and dependencies
from sqlalchemy import select
from sqlalchemy.orm import Session
from Customer_Data import (engine, NameContact, AccountContact, PhoneContact)

def search_customer():
    print("===== Search Customer =====")

    # Open a connection to the database
    with Session(engine) as session:

        # Prompt the user for a search term
        search_term = input("Enter a name, email, or phone number to search: ")

        # Search for customers by name, email, or phone number
        customers = session.scalars(
            select(NameContact).where(
                (NameContact.full_name.contains(search_term)) |
                (AccountContact.email_address.contains(search_term)) |
                (PhoneContact.phone_number.contains(search_term))
            ).join(AccountContact).join(PhoneContact)
        ).all()

    # Display the search results
    if not customers:
        print("No customers found matching the search criteria.")
    else:
        print("===== Search Results =====")
        for customer in customers:
            print(f"Customer ID: {customer.id}")
            print(f"Name: {customer.full_name}")
            print("Email: " + (", ".join(session.scalars(select(AccountContact.email_address).where(
                AccountContact.customer_id == customer.id)))))
            print("Phone: " + (", ".join(session.scalars(select(PhoneContact.phone_number).where(
                PhoneContact.customer_id == customer.id)))))
            print("Vehicle: " + "Does not work yet")

# Run the program when this file is executed directly
if __name__ == "__main__":
    search_customer()