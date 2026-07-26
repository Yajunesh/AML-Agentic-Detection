import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyDetectorTool:
    @staticmethod
    def run_structuring_rules(df: pd.DataFrame) -> pd.DataFrame:
        """Rule-based tool: Identifies repeated deposits near $10,000 threshold."""
        structuring_df = df[(df["amount"] >= 8000) & (df["amount"] < 10000)].copy()
        counts = structuring_df.groupby("customer_id").size()
        suspicious_custs = counts[counts >= 3].index
        
        result = df[(df["customer_id"].isin(suspicious_custs)) & (df["amount"] >= 8000) & (df["amount"] < 10000)].copy()
        result["raw_score"] = 0.92
        result["pattern_flag"] = "STRUCTURING_SMURFING"
        return result

    @staticmethod
    def run_ml_isolation_forest(df_feat: pd.DataFrame, contamination: float = 0.03) -> pd.DataFrame:
        """ML-based tool: Unsupervised anomaly detection on behavioral features."""
        if len(df_feat) < 5:
            df_feat["raw_score"] = 0.30
            df_feat["pattern_flag"] = "INSUFFICIENT_SAMPLE_FOR_ML"
            return df_feat

        model = IsolationForest(contamination=contamination, random_state=42)
        features = ["amount", "dist_to_10k", "near_structuring_zone"]
        
        df_scored = df_feat.copy()
        df_scored["anomaly_pred"] = model.fit_predict(df_scored[features])
        
        df_scored["raw_score"] = np.where(df_scored["anomaly_pred"] == -1, 0.85, 0.15)
        df_scored["pattern_flag"] = np.where(df_scored["anomaly_pred"] == -1, "ANOMALOUS_VELOCITY_OR_AMOUNT", "BASELINE_NORMAL")
        return df_scored