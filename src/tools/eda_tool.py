import pandas as pd

class EDATool:
    @staticmethod
    def profile_dataset(df: pd.DataFrame) -> dict:
        """Profiles dataset segment and extracts top-level stats."""
        if df.empty:
            return {"error": "Dataset is empty for selected filter."}
            
        return {
            "total_transactions": len(df),
            "unique_customers": df["customer_id"].nunique(),
            "total_volume": float(df["amount"].sum()),
            "avg_transaction": float(df["amount"].mean()),
            "max_transaction": float(df["amount"].max()),
            "top_countries": df["country"].value_counts().to_dict(),
            "tx_type_breakdown": df["transaction_type"].value_counts().to_dict()
        }