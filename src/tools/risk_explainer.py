import pandas as pd

class RiskExplainerTool:
    @staticmethod
    def generate_explanations(df: pd.DataFrame) -> pd.DataFrame:
        """Maps raw scores to risk tiers, explanations, and escalation decisions."""
        if df.empty:
            return df

        results_df = df.copy()
        risk_levels, actions, explanations = [], [], []

        for _, row in results_df.iterrows():
            score = row.get("raw_score", 0.20)
            amt = row.get("amount", 0.0)
            flag = row.get("pattern_flag", "NORMAL")

            if score >= 0.85:
                level = "HIGH"
                action = "REPORT (File SAR/CTR)"
                reason = f"High-risk pattern [{flag}] detected. Transaction amount (${amt:,.2f}) sits in suspicious threshold range with elevated velocity."
            elif score >= 0.50:
                level = "MEDIUM"
                action = "FLAG FOR REVIEW"
                reason = f"Elevated risk score ({score:.2f}). Transaction displays noticeable deviation compared to baseline peer activity."
            else:
                level = "LOW"
                action = "MONITOR"
                reason = "Minor variance observed; remains within acceptable operational risk bounds."

            risk_levels.append(level)
            actions.append(action)
            explanations.append(reason)

        results_df["risk_level"] = risk_levels
        results_df["escalation_action"] = actions
        results_df["agent_explanation"] = explanations
        return results_df