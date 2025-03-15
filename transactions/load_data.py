import os
import pandas as pd
from transactions.models import Transaction
from django.db.utils import IntegrityError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE_PATH = os.path.join(BASE_DIR, "finance_data.csv")

def load_csv_to_db():
    if not os.path.exists(CSV_FILE_PATH):
        print(f"Error: File '{CSV_FILE_PATH}' not found!")
        return

    df = pd.read_csv(CSV_FILE_PATH)

    for _, row in df.iterrows():
        date_str = str(row["date"]).strip()
        transaction_date = pd.to_datetime(date_str, format="%B %d, %Y", errors="coerce").date()

        if pd.isnull(transaction_date):  # Skip invalid date rows
            print(f"Skipping row due to invalid date format: {row}")
            continue

        try:
            # Check if transaction already exists before inserting
            if not Transaction.objects.filter(date=transaction_date, amount=row["amount"], category=row["category"], description=row["description"]).exists():
                Transaction.objects.create(
                    date=transaction_date,
                    amount=row["amount"],
                    category=row["category"],
                    description=row["description"]
                )
                print(f"Inserted: {transaction_date} - {row['amount']} - {row['category']} - {row['description']}")
            else:
                print(f"Skipping duplicate: {transaction_date} - {row['amount']} - {row['category']} - {row['description']}")

        except IntegrityError:
            print(f"Error inserting row: {row}")

    print("✅ Data loaded successfully without duplicates!")
    