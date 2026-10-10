
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

# Create the database
engine = create_engine("sqlite:///AccountContacts.db")


# Define the database table
class Base(DeclarativeBase):
    pass


class AccountContact(Base):
    __tablename__ = "account_contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(
        String(254), unique=True, nullable=False
    )


# Create the table if it does not exist
Base.metadata.create_all(engine)


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


if __name__ == "__main__":
    collect_email()
