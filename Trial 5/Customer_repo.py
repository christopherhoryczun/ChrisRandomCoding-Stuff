from sqlalchemy import select, delete, or_
from sqlalchemy.orm import Session
from Customer_Data import engine, NameContact, AccountContact, PhoneContact


# Builds a plain dictionary for one customer, including emails and phones.
def _customer_to_dict(session, customer):
    emails = session.scalars(
        select(AccountContact.email_address)
        .where(AccountContact.customer_id == customer.id)).all()
    phones = session.scalars(
        select(PhoneContact.phone_number)
        .where(PhoneContact.customer_id == customer.id)).all()
    return {
        "id": customer.id,
        "full_name": customer.full_name,
        "emails": list(emails),
        "phones": list(phones),
    }


# Creates and stores a new customer record in the database.
def add_customer(name, email, phone):
    with Session(engine) as session:
        # Create the customer record first
        customer = NameContact(full_name=name)
        session.add(customer)

        # Generate the customer ID before adding related records
        session.flush()
        customer_id = customer.id

        # Save the customer's email with the same customer ID
        session.add(AccountContact(email_address=email, customer_id=customer_id))

        # Save the customer's phone with the same customer ID
        session.add(PhoneContact(phone_number=phone, customer_id=customer_id))

        session.commit()
        return customer_id


# Retrieves a single customer record using its unique customer ID.
def get_customer_by_id(customer_id):
    with Session(engine) as session:
        customer = session.get(NameContact, customer_id)
        if customer is None:
            return None
        return _customer_to_dict(session, customer)


# Retrieves the customer records currently stored in the database.
def list_customers():
    return search_customers()


# Retrieves customer records matching the provided search criteria.
def search_customers(term=""):
    with Session(engine) as session:
        query = select(NameContact).order_by(NameContact.id)

        if term:
            like = f"%{term}%"
            query = (query
                     .outerjoin(AccountContact, AccountContact.customer_id == NameContact.id)
                     .outerjoin(PhoneContact, PhoneContact.customer_id == NameContact.id)
                     .where(or_(NameContact.full_name.ilike(like),
                                AccountContact.email_address.ilike(like),
                                PhoneContact.phone_number.ilike(like)))
                     .distinct())

        customers = session.scalars(query).all()
        return [_customer_to_dict(session, c) for c in customers]


# Deletes a customer record from the database after the service layer has determined that removal is permitted.
def delete_customer(customer_id):
    with Session(engine) as session:
        customer = session.get(NameContact, customer_id)
        if customer is None:
            return False

        # Remove the related records first, then the customer
        session.execute(delete(AccountContact).where(AccountContact.customer_id == customer_id))
        session.execute(delete(PhoneContact).where(PhoneContact.customer_id == customer_id))
        session.delete(customer)

        session.commit()
        return True
