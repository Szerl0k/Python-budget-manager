import json
import random
import os
from datetime import datetime, timedelta

from src.models import Transaction, CATEGORIES

def generate_example_json(path: str="data/example_data.json", count: int = 10):
    if os.path.isfile("path"):
        print(f"{path} already exists")
    else:

        transactions = []

        start_date = datetime.now() - timedelta(days=90)
        for i in range(count):
            trans_date = (start_date + timedelta(days=random.randint(0, 90))).strftime("%Y-%m-%d")
            amount = round(random.uniform(-200, 2000), 2)
            trans = Transaction(
                id=i + 1,
                date=trans_date,
                category=random.choice(CATEGORIES),
                amount=amount,
                description=f"Cos"
            )
            transactions.append(trans.to_dict())


        with open(path, "w") as outfile:
            json.dump(transactions, outfile, indent=2)



