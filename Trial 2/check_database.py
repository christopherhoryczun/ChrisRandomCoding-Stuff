import sqlite3

connection = sqlite3.connect("CustomerContactInfo.db")
cursor = connection.cursor()

for table in ("name_contacts", "account_contacts", "phone_contacts"):
    cursor.execute(f"PRAGMA table_info({table})")
    print(f"\n{table}:")
    for column in cursor.fetchall():
        print(column[1], column[2])

connection.close()