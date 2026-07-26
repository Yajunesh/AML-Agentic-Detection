import pandas as pd

class FeatureEngineeringTool:
    @staticmethod
    def compute_aml_features(df: pd.DataFrame) -> pd.DataFrame:
        """Calculates proximity to $10,000 regulatory thresholds and customer transaction velocity."""
        df_feat = df.copy()
        
        # Distance to $10k regulatory threshold
        df_feat["dist_to_10k"] = 10000.0 - df_feat["amount"]
        df_feat["near_structuring_zone"] = (df_feat["amount"] >= 8000) & (df_feat["amount"] < 10000)
        
        # Chronological sorting for velocity calculations
        df_feat = df_feat.sort_values(["customer_id", "timestamp"])
        
        # Cumulative metrics per customer
        df_feat["cust_tx_count"] = df_feat.groupby("customer_id")["transaction_id"].transform("cumcount") + 1
        df_feat["cust_running_vol"] = df_feat.groupby("customer_id")["amount"].transform("cumsum")
        
        return df_feat