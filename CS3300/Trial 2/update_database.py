
import sqlite3
import shutil
import os

database = "CustomerContactInfo.db"
backup = "CustomerContactInfo_backup.db"

# Back up the database before making changes
if os.path.exists(database):
    shutil.copy2(database, backup)
    print(f"Backup created: {backup}")

connection = sqlite3.connect(database)
cursor = connection.cursor()

try:
    # Add customer_id to the email table
    cursor.execute("PRAGMA table_info(account_contacts)")
    email_columns = [column[1] for column in cursor.fetchall()]

    if "customer_id" not in email_columns:
        cursor.execute(
            "ALTER TABLE account_contacts ADD COLUMN customer_id INTEGER"
        )

    # Add customer_id to the phone table
    cursor.execute("PRAGMA table_info(phone_contacts)")
    phone_columns = [column[1] for column in cursor.fetchall()]

    if "customer_id" not in phone_columns:
        cursor.execute(
            "ALTER TABLE phone_contacts ADD COLUMN customer_id INTEGER"
        )

    connection.commit()
    print("Database updated successfully.")

except sqlite3.Error as error:
    connection.rollback()
    print(f"Database update failed: {error}")

finally:
    connection.close()

