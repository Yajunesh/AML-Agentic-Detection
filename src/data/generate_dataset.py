import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_aml_data(filepath="src/data/transactions.csv"):
    np.random.seed(42)
    n_records = 1500
    base_date = datetime(2026, 5, 1)

    customer_ids = [f"CUST_{1000 + i}" for i in range(100)]
    tx_types = ["CASH_DEPOSIT", "WIRE_TRANSFER", "ATM_WITHDRAWAL", "PAYMENT"]

    data = []
    for i in range(n_records):
        cust = np.random.choice(customer_ids)
        days_offset = np.random.randint(0, 60)
        timestamp = base_date + timedelta(days=days_offset, hours=np.random.randint(0, 24))
        tx_type = np.random.choice(tx_types)
        amount = round(np.random.exponential(scale=1500) + 10, 2)
        
        data.append({
            "transaction_id": f"TXN_{100000 + i}",
            "customer_id": cust,
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "amount": amount,
            "transaction_type": tx_type,
            "country": np.random.choice(["US", "CA", "MX", "CY", "KY"], p=[0.7, 0.15, 0.08, 0.04, 0.03])
        })
    
    df = pd.DataFrame(data)

    # Inject Structuring Pattern for CUST_1042
    for j in range(12):
        df.loc[j, "customer_id"] = "CUST_1042"
        df.loc[j, "amount"] = round(np.random.uniform(9200, 9950), 2)
        df.loc[j, "transaction_type"] = "CASH_DEPOSIT"
        df.loc[j, "timestamp"] = (base_date + timedelta(days=45, hours=j*2)).strftime("%Y-%m-%d %H:%M:%S")

    df.to_csv(filepath, index=False)
    print(f"Synthetic dataset created successfully at {filepath}")

if __name__ == "__main__":
    generate_aml_data()