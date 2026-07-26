import streamlit as st
import pandas as pd
import os

from agent.orchestrator import AMLAgentOrchestrator
from data.generate_dataset import generate_aml_data

@st.cache_data
def load_data():
    csv_path = "src/data/transactions.csv"
    if not os.path.exists(csv_path):
        os.makedirs("src/data", exist_ok=True)
        generate_aml_data(csv_path)
    
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def main():
    st.set_page_config(page_title="AI Agent AML Detector", layout="wide")
    st.title("🛡️ Autonomous AI Agent for AML Suspicious Activity Detection")

    raw_data = load_data()
    orchestrator = AMLAgentOrchestrator(raw_data)

    st.sidebar.header("🕹️ Preset Query Benchmarks")
    preset = st.sidebar.radio(
        "Select a test query:",
        [
            "Custom Query",
            "Find structuring patterns in the last 30 days",
            "Which customers made 10+ transactions under $10,000?",
            "Is customer ID CUST_1042 suspicious?"
        ]
    )

    user_query = preset if preset != "Custom Query" else st.text_input("Enter natural language instructions:", "Analyze CUST_1042 for suspicious structuring activities")

    if st.button("Run Agent Inspection", type="primary"):
        st.subheader("🤖 Agent Execution Summary")
        
        plan = orchestrator.parse_query_intent(user_query)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Parsed Entity Target", plan["entity_id"] if plan["entity_id"] else "Global / All")
        c2.metric("Target Pattern Type", plan["pattern_type"])
        c3.metric("Time Scope Filter", f"{plan['days_filter']} Days" if plan['days_filter'] else "Full Timeline")

        st.info(f"**Agent Strategy & Reasoning:** {plan['reasoning']}")

        results = orchestrator.execute_plan(plan)

        with st.expander("🔍 Internal Agent Tool Execution Logs", expanded=True):
            for log in results["logs"]:
                st.write(f"- {log}")

        if results["eda"]:
            st.subheader("📊 Exploratory Data Analysis Profile (Selectively Invoked)")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Transactions", results["eda"]["total_transactions"])
            m2.metric("Unique Accounts", results["eda"]["unique_customers"])
            m3.metric("Total Volume", f"${results['eda']['total_volume']:,.2f}")
            m4.metric("Average Ticket", f"${results['eda']['avg_transaction']:,.2f}")

        st.subheader("🚩 Suspicious Activity & Escalation Actions")
        flagged_df = results["flagged_data"]

        if not flagged_df.empty:
            cols = ["transaction_id", "customer_id", "timestamp", "amount", "risk_level", "escalation_action", "agent_explanation"]
            st.dataframe(flagged_df[[c for c in cols if c in flagged_df.columns]], use_container_width=True)
        else:
            st.success("No suspicious activity matching criteria detected.")

if __name__ == "__main__":
    main()