import os
import pandas as pd

def collect_email():
    EmailMe = True
    while EmailMe:
        email = input("Please enter your email address: ").strip()

        # See if it is a valid email address by checking for exactly one @ symbol
        if '@' not in email or email.count('@') != 1:
            print("Invalid email. Please enter a valid email address.")
            continue

        email_chain = "AccountContacts.xlsx"

        # Match the email domain to check if it is valid
        valid_extensions = (".com", ".org", ".net", ".edu", ".gov")
        if email.endswith(valid_extensions):
            # Read existing file or create a blank DataFrame if it doesn't exist
            if os.path.exists(email_chain):
                df = pd.read_excel(email_chain)
            else:
                df = pd.DataFrame(columns=["Email Address"])

            # Add the new email to the list
            new_data = pd.DataFrame([{"Email Address": email}])
            df = pd.concat([df, new_data], ignore_index=True)

            # Save the updated list back to Excel
            df.to_excel(email_chain, index=False)
            print(f"Thank you! Your email address '{email}' has been added to your account.")
            EmailMe = False
            return

        print("Invalid email domain. Please enter a valid email address ending with .com, .org, .net, .edu, or .gov.")

if __name__ == "__main__":
    collect_email()
