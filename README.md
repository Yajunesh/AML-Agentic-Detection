# AI-Powered Suspicious Activity Detection Engine

An autonomous Anti-Money Laundering (AML) compliance agent that parses natural language queries, dynamically constructs execution plans, and selectively invokes specialized micro-tools for anomaly detection, rule matching, and explainable risk escalation.

---

## 🎯 Key Features & Dynamic Execution

Unlike rigid sequential pipelines, this agent parses intent to run only the necessary tools:

1. **Structuring & Smurfing Queries:** Executes targeted threshold rules; skips broad EDA and ML pipelines for maximum speed.
2. **Single Entity Lookups:** Executes localized entity filtering and feature engineering; bypasses dataset-wide profiling.
3. **Broad Exploration Queries:** Invokes the full pipeline including EDA profiling, feature engineering, and unsupervised ML (`IsolationForest`).

---

## 🚀 Quick Start Guide & Installation

### Prerequisites

* **Python 3.9+**
* `pip` (Python package installer)

### Step 1: Clone the Repository & Navigate to Folder

```bash
git clone https://github.com/your-username/aml-agentic-detection.git
cd aml-agentic-detection
```

### Step 2: Create & Activate Virtual Environment

Setting up an isolated virtual environment is recommended to prevent dependency conflicts.

```bash
# On macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

```bash
# On Windows (Command Prompt / PowerShell)
python -m venv venv
.\venv\Scripts\activate
```

### Step 3: Install Required Dependencies

Install all required libraries using `pip`:

```bash
pip install streamlit pandas numpy scikit-learn
```

### Step 4: Launch the Streamlit Web Application

Execute the following command from the project root directory:

```bash
streamlit run src/app.py
```

> **Note:** Upon initial boot, the application automatically runs `generate_dataset.py` to create `src/data/transactions.csv` if it is not already present.

---

## 🕹️ Interactive Dashboard Usage

1. Once launched, open your web browser to `http://localhost:8501`.
2. Select **Benchmark Preset Queries** from the sidebar menu:
   * **Structuring Query:** `Find structuring patterns in the last 30 days` (triggers the Rule Engine, skips EDA/ML).
   * **Single Account Lookup:** `Is customer ID CUST_1042 suspicious?` (triggers a localized entity lookup).
   * **Broad Query:** `Perform broad suspicious activity exploration across all accounts` (triggers full EDA + ML).
3. Or enter **Custom Instructions** in natural language inside the main text field and click **Run Agent Inspection**.
4. Expand the **Agent Execution Summary** tab to inspect which tools were dynamically called or bypassed.

---

## 🛠️ Project File Tree

```text
Project/
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
```
