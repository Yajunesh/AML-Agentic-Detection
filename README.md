# AI-Powered Suspicious Activity Detection Engine

An autonomous Anti-Money Laundering (AML) compliance agent that parses natural language queries, dynamically constructs execution plans, and selectively invokes specialized micro-tools for anomaly detection, rule matching, and explainable risk escalation.

---

## 🎯 Key Features & Dynamic Execution
Unlike rigid sequential pipelines, this agent parses intent to run only necessary tools:
1. **Structuring & Smurfing Queries:** Executes targeted threshold rules; skips broad EDA and ML pipelines for maximum speed.
2. **Single Entity Lookups:** Executes localized entity filtering and feature engineering; bypasses dataset-wide profiling.
3. **Broad Exploration Queries:** Invokes full pipeline including EDA profiling, feature engineering, and unsupervised ML (`IsolationForest`).

---

## 🛠️ Project File Tree
```text
Project/
├── README.md                          # Quick start instructions & overview
├── Documentation.pdf                  # System architecture, ML specs, & UI docs
├── Presentation.pdf                   # Problem statement & solution slide deck
├── Links_And_Resources.docx           # Public GitHub & Solution Video links
└── src/
    ├── app.py                         # Streamlit Dashboard UI
    ├── agent/
    │   ├── orchestrator.py            # Dynamic Agent Orchestrator & Router
    │   └── prompt_templates.py        # Intent Parser Prompts
    ├── tools/
    │   ├── eda_tool.py                # EDA & Profiling Tool
    │   ├── feature_engineering.py     # AML Feature Engineering Engine
    │   ├── anomaly_detector.py        # Hybrid Anomaly Detection (Rules + Isolation Forest)
    │   └── risk_explainer.py          # Explainability & Escalation Tool
    └── data/
        └── generate_dataset.py        # Synthetic Data Generator
