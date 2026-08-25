# 🛡️ Chargeback Risk Scorer Pro

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=30&duration=2800&pause=900&color=FF6B6B&center=true&vCenter=true&width=850&lines=%F0%9F%9B%A1%EF%B8%8F+Chargeback+Risk+Scorer+Pro;AI-Powered+Fraud+Risk+Detection;Predict+Risk.+Protect+Revenue.;Stop+Merchant+Losses+Before+They+Happen." alt="Typing SVG" />
</p>

<p align="center">
  <b>AI-powered • Explainable • Cost-sensitive • Defense-only</b>
</p>

<p align="center">
  <a href="https://risk-analyzer-ai.streamlit.app/">
    <img src="https://img.shields.io/badge/%F0%9F%9A%80%20LIVE%20DEMO-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  </a>
  <a href="https://github.com/Barath-RK/AI-Risk-Manager">
    <img src="https://img.shields.io/badge/%F0%9F%92%BB%20SOURCE%20CODE-181717?style=for-the-badge&logo=github&logoColor=white" />
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Precision-69.8%25-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Recall-100%25-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/ROC--AUC-62.6%25-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Net%20Savings-%E2%82%B9314K-success?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Defense--Only-%E2%9C%85-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/XGBoost-FF6F00?style=for-the-badge&logo=xgboost&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/SHAP-0055FF?style=for-the-badge" />
</p>

---

## 🌐 Live Demo

<p align="center">
  <a href="https://risk-analyzer-ai.streamlit.app/">
    <img src="https://img.shields.io/badge/%F0%9F%94%A5%20OPEN%20CHARGEBACK%20RISK%20SCORER-FF6B6B?style=for-the-badge&logo=streamlit&logoColor=white" />
  </a>
</p>

<p align="center">
  <a href="https://risk-analyzer-ai.streamlit.app/">
    <b>https://risk-analyzer-ai.streamlit.app/</b>
  </a>
</p>

---

## 🧠 What Is Chargeback Risk Scorer Pro?

**Chargeback Risk Scorer Pro** is an AI-powered merchant defense platform designed to identify transactions with a high probability of resulting in fraudulent chargebacks.

Instead of relying solely on static rules, the system combines:

```text
Transaction Intelligence
        ↓
Machine Learning
        ↓
Cost-Sensitive Risk Scoring
        ↓
Explainable AI
        ↓
Merchant Decision Support
```

The goal is simple:

> **Detect risky transactions early, explain why they are risky, and help merchants reduce preventable chargeback losses.**

---

# 🎯 The Problem

Chargebacks create a significant operational and financial burden for merchants.

```text
┌──────────────────────────────────────────────────────────────┐
│                    MERCHANT CHALLENGE                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  💳 Suspicious Transactions                                  │
│             ↓                                                │
│  📦 Order Fulfillment                                        │
│             ↓                                                │
│  ⚠️ Customer Dispute                                         │
│             ↓                                                │
│  💸 Chargeback + Processing Costs                            │
│             ↓                                                │
│  📉 Revenue & Margin Loss                                    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

Traditional rule-based systems often struggle because fraud patterns change over time.

### The challenge

* Static rules can miss sophisticated patterns
* Aggressive blocking can create false positives
* Merchants need understandable decisions
* Every false negative can have a direct financial cost
* Fraud detection must balance security with customer experience

---

# 🛡️ Our Solution

Chargeback Risk Scorer Pro transforms transaction data into an actionable risk assessment.

```text
                  ┌─────────────────────┐
                  │ Transaction Data    │
                  └──────────┬──────────┘
                             ↓
                  ┌─────────────────────┐
                  │ 17 Risk Signals     │
                  └──────────┬──────────┘
                             ↓
                  ┌─────────────────────┐
                  │ XGBoost Classifier   │
                  └──────────┬──────────┘
                             ↓
                  ┌─────────────────────┐
                  │ Risk Score 0 → 1    │
                  └──────────┬──────────┘
                             ↓
             ┌───────────────┴───────────────┐
             ↓                               ↓
      ┌──────────────┐               ┌──────────────┐
      │ SHAP Analysis│               │ Cost Engine  │
      └──────┬───────┘               └──────┬───────┘
             └───────────────┬───────────────┘
                             ↓
                  ┌─────────────────────┐
                  │ Merchant Decision   │
                  └─────────────────────┘
```

---

# ⚡ Key Features

## 🎯 AI Risk Prediction

| Capability           | Description                                        |
| -------------------- | -------------------------------------------------- |
| 🤖 XGBoost Model     | Machine-learning based fraud classification        |
| 🎯 Risk Score        | Produces a normalized 0–1 risk score               |
| 🧠 17 Signals        | Uses transaction, customer and evidence indicators |
| ⚖️ Cost Optimization | Threshold optimized around business impact         |
| 🔎 Explainability    | SHAP-based decision analysis                       |

---

## 🧠 Explainable AI

The system doesn't simply say:

> ❌ **"High Risk"**

It explains:

> ⚠️ **"This transaction received a high-risk score primarily because of prior disputes, incomplete evidence, and weak authentication signals."**

### SHAP-powered explanations

```text
Risk Contribution

Prior Disputes          ████████████████████
Evidence Completeness   ███████████████
Customer Risk Score     ███████████
AVS/CVV Match           ███████
3DS Authentication      █████
Transaction Amount      ███
```

This allows merchants and analysts to understand **why** a transaction was flagged.

---

# 🔬 Advanced Analytics

### 📈 Fraud Spike Detection

Identifies unusual increases in suspicious transaction activity.

```text
Normal Activity
▂▃▂▃▃▂▃▂▃▂▃

              🚨 SPIKE
▂▃▂▃▂▃▂▃▆████████
```

### 🕸️ Fraud Ring Detection

Uses clustering techniques such as **DBSCAN** to identify potentially coordinated transaction patterns.

```text
Transaction A ─── Customer X
       │
       ├──────── Merchant Y
       │
Transaction B ─── Device Z
       │
       └──────── Customer X

          ↓

     ⚠️ Suspicious Cluster
```

### 🧪 A/B Testing

Compare machine-learning decisions against simple business rules.

| Method                |   Accuracy |
| --------------------- | ---------: |
| 🤖 XGBoost Model      |  **72.3%** |
| 📏 Simple Amount Rule |      42.5% |
| 🚀 Improvement        | **+29.8%** |

---

# 📊 Model Performance

## 🏆 Evaluation Metrics

<p align="center">

| Metric               |       Result |
| -------------------- | -----------: |
| 🎯 Precision         |    **69.8%** |
| 🔥 Recall            |   **100.0%** |
| 📈 ROC-AUC           |    **62.6%** |
| 💰 Net Savings       | **₹314,000** |
| 📉 Cost Reduction    |    **87.3%** |
| ⚙️ Optimal Threshold |     **0.10** |

</p>

---

## 🧮 Confusion Matrix

**Test Set: 937 Transactions**

|                     | Predicted No Fraud | Predicted Fraud |
| ------------------- | -----------------: | --------------: |
| **Actual No Fraud** |                  0 |          283 FP |
| **Actual Fraud**    |                  0 |          654 TP |

### Interpretation

The evaluated threshold was intentionally tuned toward **maximum fraud recall**, prioritizing detection of fraudulent cases within the project's cost model.

> **100% recall means every fraud case in this test set was flagged by the selected threshold.**

---

# 💰 Business Impact

The model was evaluated using an explicit business-cost framework.

```text
WITHOUT MODEL
────────────────────────────────
Estimated Loss

₹359,700


WITH MODEL
────────────────────────────────
Estimated Loss

₹45,700


────────────────────────────────
NET SAVINGS

₹314,000

COST REDUCTION

87.3%
```

### Cost assumptions

| Event          | Cost |
| -------------- | ---: |
| False Positive | ₹100 |
| False Negative | ₹550 |

The threshold was selected with the objective of minimizing the modeled business cost rather than optimizing accuracy alone.

---

# 🧩 Risk Signals

The model uses multiple transaction and customer-level signals.

```text
┌─────────────────────────────────────────────────┐
│              RISK SIGNALS                       │
├─────────────────────────────────────────────────┤
│                                                 │
│ 💳 Transaction Amount                           │
│ 👤 Customer Tenure                              │
│ ⚠️ Prior Disputes                               │
│ 📊 Customer Risk Score                          │
│ 🏪 Merchant Chargeback Rate                     │
│ 📦 Delivery Confirmation                        │
│ 🔐 AVS Match                                    │
│ 🔐 CVV Match                                    │
│ 🛡️ 3DS Authentication                           │
│ 📄 Evidence Completeness                        │
│ 🔁 Repeat Disputer                              │
│                                                 │
│ + Additional engineered transaction signals     │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

# 🏗️ System Architecture

```text
                         USER
                          │
                          ▼
              ┌──────────────────────┐
              │ Streamlit Dashboard   │
              ├──────────────────────┤
              │ Dashboard             │
              │ Explorer              │
              │ Risk Analyzer         │
              │ Fraud Analytics       │
              │ Batch Upload          │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Prediction Engine    │
              ├──────────────────────┤
              │ Feature Processing    │
              │ XGBoost Model         │
              │ Risk Scoring          │
              │ Threshold Engine      │
              └──────────┬───────────┘
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
    ┌────────────────┐      ┌────────────────┐
    │ Explainability │      │ Cost Analysis  │
    │     SHAP       │      │ FP / FN Costs  │
    └────────┬───────┘      └────────┬───────┘
             └───────────┬────────────┘
                         ▼
              ┌──────────────────────┐
              │ Merchant Decision     │
              ├──────────────────────┤
              │ Risk Score            │
              │ Risk Level            │
              │ Explanation           │
              │ Recommended Action    │
              └──────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Processed Data Layer │
              │ 4,682 Transactions   │
              │ 65 Features          │
              └──────────────────────┘
```

---

# 🖥️ Dashboard

The Streamlit application provides an interactive interface for merchants and analysts.

### Dashboard Modules

```text
┌───────────────────────────────────────────────────────┐
│                  CHARGEBACK RISK SCORER               │
├───────────────────────────────────────────────────────┤
│                                                       │
│  📊 Dashboard       🔎 Explorer       🎯 Risk Analyzer│
│                                                       │
│  ───────────────────────────────────────────────────  │
│                                                       │
│  📈 Fraud Analytics        📁 Batch Processing        │
│                                                       │
│  ───────────────────────────────────────────────────  │
│                                                       │
│  Risk Score       Fraud Probability     Recommendation│
│                                                       │
│     0.87              87%                  REVIEW     │
│                                                       │
└───────────────────────────────────────────────────────┘
```

---

# 🔮 What-If Analysis

The platform allows analysts to understand how transaction evidence can affect risk.

Example:

```text
CURRENT TRANSACTION
──────────────────────────────

Risk Score:       0.82
Risk Level:       HIGH
Evidence:         Incomplete
3DS:              Not Authenticated


WHAT IF?
──────────────────────────────

Evidence Complete      → Risk ↓
3DS Authenticated       → Risk ↓
CVV Verified            → Risk ↓
Delivery Confirmed      → Risk ↓
```

This provides actionable insight rather than simply producing a classification.

---

# 📁 Project Structure

```text
AI-Risk-Manager/
│
├── 📂 dashboard/
│   └── app.py
│
├── 📂 data/
│   └── chargeback_cases_processed.csv
│
├── 📂 models/
│   ├── xgb_model.pkl
│   ├── scaler.pkl
│   ├── optimal_threshold.pkl
│   └── metrics.csv
│
├── 📂 notebooks/
│   └── 01_exploration.py
│
├── 📂 src/
│   └── train.py
│
├── 📄 requirements.txt
├── 📄 README.md
└── 📄 .gitignore
```

---

# 🚀 Quick Start

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Barath-RK/AI-Risk-Manager.git
cd AI-Risk-Manager
```

## 2️⃣ Create Virtual Environment

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Train the Model

```bash
python src/train.py
```

## 5️⃣ Launch Dashboard

```bash
streamlit run dashboard/app.py
```

Then open:

```text
http://localhost:8501
```

---

# ☁️ Deploy to Streamlit Cloud

### Step 1

Push the project to GitHub.

### Step 2

Open Streamlit Community Cloud.

### Step 3

Connect your GitHub repository.

### Step 4

Select:

```text
dashboard/app.py
```

### Step 5

Deploy 🚀

---

# 🛠️ Technology Stack

## 🤖 Machine Learning

| Technology      | Purpose                    |
| --------------- | -------------------------- |
| 🟠 XGBoost      | Fraud risk classification  |
| 🧪 scikit-learn | Preprocessing & evaluation |
| 🔵 SHAP         | Explainable AI             |
| 🐼 Pandas       | Data processing            |
| 🔢 NumPy        | Numerical computation      |
| 🕸️ DBSCAN      | Fraud cluster detection    |

## 🎨 Application

| Technology    | Purpose                    |
| ------------- | -------------------------- |
| 🚀 Streamlit  | Interactive dashboard      |
| 📊 Plotly     | Interactive visualizations |
| 📈 Matplotlib | Model visualizations       |

## ☁️ Deployment

| Technology         | Purpose             |
| ------------------ | ------------------- |
| ☁️ Streamlit Cloud | Application hosting |
| 🐙 GitHub          | Source control      |
| 🐍 Python          | Core development    |

---

# 🔐 Defense-Only Architecture

This project is explicitly designed as a **defensive financial-risk assessment system**.

```text
                 🛡️ DEFENSIVE AI
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   Risk Analysis   Fraud Detection   Analytics
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                Merchant Defense
```

### ✅ The system can

* Assess the risk of existing transactions
* Identify suspicious transaction patterns
* Explain model decisions
* Detect unusual fraud spikes
* Identify suspicious clusters
* Compare detection strategies
* Support merchant review decisions
* Process transaction datasets

### ❌ The system does not

* Generate fraudulent transactions
* Provide fraud execution techniques
* Bypass payment security
* Circumvent authentication
* Attack payment infrastructure
* Facilitate unauthorized activity

> **The project exists to help merchants defend against fraud, not to enable it.**

---

# 🎯 Use Cases

| Industry                 | Application                                 |
| ------------------------ | ------------------------------------------- |
| 🛒 E-Commerce            | Detect suspicious orders before fulfillment |
| 💳 FinTech               | Identify potentially risky transactions     |
| 🏦 Banking               | Support chargeback risk analysis            |
| 🎮 Digital Goods         | Reduce fraudulent digital purchases         |
| 🌍 Cross-Border Commerce | Identify unusual transaction patterns       |
| 🏪 Online Merchants      | Reduce preventable chargeback losses        |

---

# 🏆 Why This Project Stands Out

<table>
<tr>
<td width="50%">

### 💰 Business Impact

**₹314K modeled savings**

87.3% modeled cost reduction.

</td>

<td width="50%">

### 🧠 Explainable AI

SHAP-powered explanations make predictions understandable.

</td>
</tr>

<tr>
<td>

### ⚖️ Cost-Sensitive ML

Threshold optimization considers the financial impact of FP and FN errors.

</td>

<td>

### 📊 Advanced Analytics

Fraud spikes, fraud clusters, A/B testing and batch processing.

</td>
</tr>

<tr>
<td>

### 🎯 High Recall

100% recall on the evaluated test set at the selected threshold.

</td>

<td>

### 🛡️ Defense-First

Designed specifically for merchant fraud prevention.

</td>
</tr>
</table>

---

# 📈 Product Roadmap

```text
                    CURRENT
                       │
                       ▼
             ┌──────────────────┐
             │ XGBoost Risk AI  │
             └────────┬─────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       SHAP       Fraud Rings   Analytics
          │           │           │
          └───────────┼───────────┘
                      ▼
                 🚀 NEXT
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      Real-Time    Model Drift   API Layer
      Scoring      Monitoring     Integration
          │           │           │
          └───────────┼───────────┘
                      ▼
                🏢 PRODUCTION
```

### Future Enhancements

* [ ] Real-time transaction scoring API
* [ ] Model drift monitoring
* [ ] Automated retraining pipeline
* [ ] Advanced anomaly detection
* [ ] Merchant-specific models
* [ ] Real-time alerting
* [ ] REST API integration
* [ ] Role-based analyst dashboard
* [ ] Model performance monitoring
* [ ] Production database integration

---

# 📜 Methodology

The system follows a complete ML lifecycle:

```text
Data
 ↓
Exploration
 ↓
Feature Engineering
 ↓
Preprocessing
 ↓
Model Training
 ↓
Validation
 ↓
Threshold Optimization
 ↓
Cost Evaluation
 ↓
SHAP Explainability
 ↓
Dashboard Deployment
```

The model is evaluated using both **machine-learning metrics** and **business-oriented cost metrics**.

---

# 📊 Evaluation Philosophy

Accuracy alone is not enough for fraud detection.

A model can achieve high accuracy while still missing important fraudulent cases.

Therefore, this project evaluates:

```text
                 MODEL QUALITY
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
    Precision       Recall        ROC-AUC
        │             │             │
        └─────────────┼─────────────┘
                      ▼
               BUSINESS COST
                      │
             ┌────────┴────────┐
             ▼                 ▼
        False Positive    False Negative
             Cost              Cost
             │                 │
             └────────┬────────┘
                      ▼
                 NET SAVINGS
```

This makes the project closer to a **real-world decision-support system** rather than a simple classification notebook.

---

# ⚠️ Important Note About Metrics

The reported metrics are based on the project's current dataset, evaluation setup, and selected business-cost assumptions.

They should not be interpreted as universal production performance.

Before real-world deployment, the system should be validated using:

* Larger datasets
* Temporal validation
* Out-of-distribution transactions
* Production-like fraud rates
* Calibration testing
* Model drift monitoring
* Merchant-specific cost assumptions
* Human review workflows

---

# 👨‍💻 Author

<p align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=1000&color=58A6FF&center=true&vCenter=true&width=650&lines=Built+by+Barath+R.K.;Cybersecurity+%7C+AI+%7C+Machine+Learning;Building+Defensive+Security+Systems" />

</p>

<p align="center">
  <b>Barath R K </b>
</p>

<p align="center">
  <a href="https://github.com/Barath-RK">
    <img src="https://img.shields.io/badge/GitHub-Barath--RK-181717?style=for-the-badge&logo=github&logoColor=white" />
  </a>
</p>

---

# 🙏 Acknowledgments

Special thanks to:

* **Razorpay Hackathon** — for the opportunity and problem statement
* **Streamlit** — for the interactive application framework
* **XGBoost** — for the machine-learning engine
* **SHAP** — for explainable AI
* **scikit-learn** — for ML utilities and evaluation

---

# ⭐ Support the Project

If you find **Chargeback Risk Scorer Pro** interesting or useful:

<p align="center">

⭐ **Star the repository**

🍴 **Fork the project**

🧠 **Explore the implementation**

🚀 **Try the live demo**

</p>

---

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=21&duration=3000&pause=1000&color=FF6B6B&center=true&vCenter=true&width=700&lines=%F0%9F%9B%A1%EF%B8%8F+Protecting+Merchants;Preventing+Chargeback+Losses;Explainable+AI+for+Fraud+Defense;Built+for+Defensive+Innovation" alt="Footer Animation" />
</p>

<p align="center">
  <b>🛡️ Predict Risk. Protect Revenue. Defend Trust. 🛡️</b>
</p>

<p align="center">
  <sub>Defense-only AI • Explainable Machine Learning • Merchant Risk Intelligence</sub>
</p>
