import os
import pandas as pd

def collect_number():
    CallMe = True
    while CallMe:
        phone_number = input("Please enter your Phone Number: ").strip()

        # See if it is a valid phone number by checking for only digits and optional parentheses, spaces, and hyphens
        if not phone_number.replace('(', '').replace(')', '').replace(' ', '').replace('-', '').isdigit():
            print("Invalid phone number. Please enter a valid phone number.")
            continue

        phone_chain = "AccountContacts.xlsx"

        # Read existing file or create a blank DataFrame if it doesn't exist
        if os.path.exists(phone_chain):
            df = pd.read_excel(phone_chain)
        else:
            df = pd.DataFrame(columns=["Phone Number"])

        # Add the new phone number to the list
        new_data = pd.DataFrame([{"Phone Number": phone_number}])
        df = pd.concat([df, new_data], ignore_index=True)

        # Save the updated list back to Excel
        df.to_excel(phone_chain, index=False)
        print(f"Thank you! Your phone number '{phone_number}' has been added to your account.")
        CallMe = False
        return

    print("Invalid phone number. Please enter a valid phone number.")

if __name__ == "__main__":
    collect_numbers()
