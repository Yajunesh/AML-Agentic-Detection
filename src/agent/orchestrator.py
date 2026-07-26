import re
from datetime import datetime, timedelta
import pandas as pd

from tools.eda_tool import EDATool
from tools.feature_engineering import FeatureEngineeringTool
from tools.anomaly_detector import AnomalyDetectorTool
from tools.risk_explainer import RiskExplainerTool

class AMLAgentOrchestrator:
    def __init__(self, raw_df: pd.DataFrame):
        self.raw_df = raw_df

    def parse_query_intent(self, query: str) -> dict:
        """Parses natural language query to dynamically decide tool pipeline."""
        query_lower = query.lower()
        plan = {
            "entity_id": None,
            "days_filter": None,
            "pattern_type": "GENERAL",
            "tools_to_run": [],
            "reasoning": ""
        }

        # 1. Detect Customer Entity
        cust_match = re.search(r'cust_\d+', query_lower)
        if cust_match:
            plan["entity_id"] = cust_match.group(0).upper()

        # 2. Detect Time Filters
        days_match = re.search(r'last (\d+) days', query_lower)
        if days_match:
            plan["days_filter"] = int(days_match.group(1))

        # 3. Dynamic Execution Routing
        if any(term in query_lower for term in ["structuring", "smurf", "10,000", "10000"]):
            plan["pattern_type"] = "STRUCTURING"
            plan["tools_to_run"] = ["filter_data", "structuring_rules", "explain_and_escalate"]
            plan["reasoning"] = "Structuring/threshold query detected. Executing rule-based filtering and skipping full ML/EDA pipeline for high speed."

        elif plan["entity_id"]:
            plan["pattern_type"] = "SINGLE_ENTITY"
            plan["tools_to_run"] = ["entity_lookup", "feature_eng", "anomaly_ml", "explain_and_escalate"]
            plan["reasoning"] = f"Single entity query targeted on {plan['entity_id']}. Bypassing dataset-wide EDA to run localized risk scoring."

        else:
            plan["pattern_type"] = "BROAD_EXPLORATION"
            plan["tools_to_run"] = ["filter_data", "run_eda", "feature_eng", "anomaly_ml", "explain_and_escalate"]
            plan["reasoning"] = "Broad exploratory query. Invoking full pipeline: EDA, Feature Engineering, and Machine Learning."

        return plan

    def execute_plan(self, plan: dict) -> dict:
        """Executes selected tools based on the dynamic plan."""
        df = self.raw_df.copy()
        execution_logs = []

        # 1. Filter Data
        if plan["days_filter"]:
            cutoff = datetime(2026, 7, 26) - timedelta(days=plan["days_filter"])
            df = df[df["timestamp"] >= cutoff]
            execution_logs.append(f"Applied time filter: Last {plan['days_filter']} days ({len(df)} records remaining).")

        if plan["entity_id"]:
            df = df[df["customer_id"] == plan["entity_id"]]
            execution_logs.append(f"Applied entity filter: {plan['entity_id']} ({len(df)} records found).")

        results = {"logs": execution_logs, "eda": None, "flagged_data": pd.DataFrame()}

        # 2. Invoke Targeted Micro-Tools
        if "run_eda" in plan["tools_to_run"]:
            results["eda"] = EDATool.profile_dataset(df)
            execution_logs.append("Tool Invoked: EDA & Dataset Profiler")

        if "structuring_rules" in plan["tools_to_run"]:
            flagged = AnomalyDetectorTool.run_structuring_rules(df)
            execution_logs.append("Tool Invoked: Rule Engine (Structuring & Smurfing)")
            results["flagged_data"] = flagged

        elif "anomaly_ml" in plan["tools_to_run"]:
            feat_df = FeatureEngineeringTool.compute_aml_features(df)
            execution_logs.append("Tool Invoked: Feature Engineering Engine")
            
            scored_df = AnomalyDetectorTool.run_ml_isolation_forest(feat_df)
            execution_logs.append("Tool Invoked: Machine Learning Anomaly Detector (Isolation Forest)")
            
            flagged = scored_df[scored_df["raw_score"] > 0.5].copy()
            results["flagged_data"] = flagged

        # 3. Explainability Layer
        if "explain_and_escalate" in plan["tools_to_run"] and not results["flagged_data"].empty:
            results["flagged_data"] = RiskExplainerTool.generate_explanations(results["flagged_data"])
            execution_logs.append("Tool Invoked: Risk Classification & Natural Language Explainer")

        return results