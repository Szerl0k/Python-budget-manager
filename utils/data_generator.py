import json
import random
import os
from datetime import datetime, timedelta

from models.transaction import Transaction, CATEGORIES

def generate_example_json(path: str="../data/test_data.json", count: int = 10):
    if os.path.isfile("path"):
        print(f"{path} already exists")
    else:

        transactions = []

        start_date = datetime.now() - timedelta(days=90)
        for i in range(count):
            trans_date = (start_date + timedelta(days=random.randint(0, 90)))
            amount = round(random.uniform(-2000, 2000), 2)


            if amount > 0:
                category = "Wynagrodzenie"
            else:
                other_categories = [c for c in CATEGORIES if c != "Wynagrodzenie"]
                category = random.choice(other_categories)

            trans = Transaction(
                id=i + 1,
                date=trans_date,
                category=category,
                amount=amount,
                description="Empty",
                is_euro=random.choice([True, False])
            )
            transactions.append(trans.to_dict())


        with open(path, "w") as outfile:
            json.dump(transactions, outfile, indent=2)



