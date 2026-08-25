import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="Chargeback Risk Scorer",
    page_icon="🛡️",
    layout="wide"
)

# Load models and data
@st.cache_resource
def load_resources():
    model = joblib.load('models/xgb_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    threshold = joblib.load('models/optimal_threshold.pkl')
    metrics = pd.read_csv('models/metrics.csv').iloc[0]
    df = pd.read_csv('data/chargeback_cases_processed.csv')
    return model, scaler, threshold, metrics, df

try:
    model, scaler, threshold, metrics, df = load_resources()
except:
    st.error("Please run src/train.py first to train the model!")
    st.stop()

# Feature list
FEATURES = [
    'transaction_amount', 'customer_tenure_months', 'customer_prior_disputes',
    'customer_risk_score', 'merchant_chargeback_rate', 'merchant_monthly_volume',
    'is_cross_border', 'is_digital_goods', 'days_to_dispute',
    'has_delivery_tracking', 'has_delivery_confirmation', 'has_avs_match',
    'has_cvv_match', 'has_3ds_authentication', 'evidence_completeness',
    'evidence_score', 'is_repeat_disputer'
]

# Sidebar navigation
st.sidebar.title("🛡️ Navigation")
page = st.sidebar.radio("Go to", ["📊 Dashboard", "🔍 Transaction Explorer", "🧠 Risk Analyzer"])

# DASHBOARD PAGE
if page == "📊 Dashboard":
    st.title("📊 Chargeback Risk Scorer Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Precision", f"{metrics['precision']:.2%}")
    with col2:
        st.metric("Recall", f"{metrics['recall']:.2%}")
    with col3:
        st.metric("ROC-AUC", f"{metrics['auc']:.2%}")
    with col4:
        st.metric("Net Savings", f"₹{metrics['savings']:,.0f}")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Confusion Matrix")
        cm_data = pd.DataFrame(
            [[metrics['tn'], metrics['fp']], [metrics['fn'], metrics['tp']]],
            index=['Predicted No Fraud', 'Predicted Fraud'],
            columns=['Actual No Fraud', 'Actual Fraud']
        )
        fig = px.imshow(cm_data, text_auto=True, color_continuous_scale='Blues')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Risk Score Distribution")
        X = df[FEATURES]
        X_scaled = scaler.transform(X)
        risk_scores = model.predict_proba(X_scaled)[:, 1]
        
        fig = px.histogram(risk_scores, nbins=50, title="Risk Score Distribution")
        fig.add_vline(x=threshold, line_dash="dash", line_color="red", annotation_text=f"Threshold: {threshold:.2f}")
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("💰 Cost Analysis")
        fig = go.Figure(data=[
            go.Bar(name='Without Model', x=['Cost'], y=[metrics['fn'] * metrics['fn_cost']]),
            go.Bar(name='With Model', x=['Cost'], y=[(metrics['fp'] * metrics['fp_cost']) + (metrics['fn'] * metrics['fn_cost'])])
        ])
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🛡️ Fraud Detection")
        fraud_caught_pct = (metrics['tp'] / (metrics['tp'] + metrics['fn'])) * 100 if (metrics['tp'] + metrics['fn']) > 0 else 0
        st.metric("Fraud Caught", f"{metrics['tp']:,}", delta=f"{fraud_caught_pct:.1f}% of all fraud")
    
    with col3:
        st.subheader("🎯 False Positives")
        fp_pct = (metrics['fp'] / (metrics['fp'] + metrics['tn'])) * 100 if (metrics['fp'] + metrics['tn']) > 0 else 0
        st.metric("False Positives", f"{metrics['fp']:,}", delta=f"{fp_pct:.1f}% of legitimate", delta_color="off")

# TRANSACTION EXPLORER
elif page == "🔍 Transaction Explorer":
    st.title("🔍 Transaction Explorer")
    
    X = df[FEATURES]
    X_scaled = scaler.transform(X)
    risk_scores = model.predict_proba(X_scaled)[:, 1]
    
    df_display = df.copy()
    df_display['risk_score'] = risk_scores
    df_display['risk_level'] = df_display['risk_score'].apply(
        lambda x: 'HIGH' if x >= threshold else ('MEDIUM' if x >= threshold*0.7 else 'LOW')
    )
    df_display['recommendation'] = df_display['risk_score'].apply(
        lambda x: '⚡ REPRESENT' if x >= threshold else ('⚠️ ESCALATE' if x >= threshold*0.7 else '✅ REFUND')
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        risk_filter = st.selectbox("Risk Level", ["All", "HIGH", "MEDIUM", "LOW"])
    with col2:
        amount_range = st.slider("Transaction Amount", 0, 50000, (0, 50000))
    with col3:
        outcome_filter = st.selectbox("Recommendation", ["All", "⚡ REPRESENT", "⚠️ ESCALATE", "✅ REFUND"])
    
    filtered = df_display.copy()
    if risk_filter != "All":
        filtered = filtered[filtered['risk_level'] == risk_filter]
    filtered = filtered[(filtered['transaction_amount'] >= amount_range[0]) & (filtered['transaction_amount'] <= amount_range[1])]
    if outcome_filter != "All":
        filtered = filtered[filtered['recommendation'] == outcome_filter]
    
    st.subheader(f"Showing {len(filtered)} transactions")
    
    display_cols = ['transaction_amount', 'customer_prior_disputes', 'merchant_chargeback_rate', 
                   'evidence_score', 'risk_score', 'risk_level', 'recommendation']
    st.dataframe(
        filtered[display_cols].head(50).style.background_gradient(subset=['risk_score'], cmap='RdYlGn_r'),
        use_container_width=True
    )

# RISK ANALYZER
else:
    st.title("🧠 Risk Analyzer")
    
    st.markdown("""
    ### How this works
    Enter transaction details to get:
    1. **Risk Score**: Probability of fraudulent chargeback (0-1)
    2. **Recommendation**: REPRESENT (fight it) or REFUND (accept loss)
    3. **Key Drivers**: What features influenced the decision
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Transaction Details")
        amount = st.number_input("Transaction Amount (₹)", min_value=0, max_value=100000, value=5000)
        days_to_dispute = st.slider("Days to Dispute", 0, 180, 30)
        is_cross_border = st.selectbox("Cross Border", [0, 1], format_func=lambda x: "Yes" if x else "No")
        is_digital_goods = st.selectbox("Digital Goods", [0, 1], format_func=lambda x: "Yes" if x else "No")
        is_repeat_disputer = st.selectbox("Repeat Disputer", [0, 1], format_func=lambda x: "Yes" if x else "No")
    
    with col2:
        st.subheader("Customer & Merchant")
        customer_tenure = st.slider("Customer Tenure (months)", 0, 60, 12)
        prior_disputes = st.slider("Prior Disputes", 0, 20, 0)
        customer_risk = st.slider("Customer Risk Score", 0, 100, 50)
        merchant_chargeback_rate = st.slider("Merchant Chargeback Rate", 0, 100, 5)
        merchant_volume = st.slider("Merchant Monthly Volume", 0, 100000, 5000)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Evidence")
        delivery_tracking = st.selectbox("Delivery Tracking", [0, 1], format_func=lambda x: "Yes" if x else "No")
        delivery_confirmation = st.selectbox("Delivery Confirmation", [0, 1], format_func=lambda x: "Yes" if x else "No")
        avs_match = st.selectbox("AVS Match", [0, 1], format_func=lambda x: "Yes" if x else "No")
        cvv_match = st.selectbox("CVV Match", [0, 1], format_func=lambda x: "Yes" if x else "No")
        auth_3ds = st.selectbox("3DS Authentication", [0, 1], format_func=lambda x: "Yes" if x else "No")
        evidence_completeness = st.slider("Evidence Completeness", 0, 100, 50) / 100
    
    if st.button("🔍 Analyze Risk", type="primary"):
        evidence_score = (
            0.3 * delivery_confirmation +
            0.2 * avs_match +
            0.2 * cvv_match +
            0.15 * auth_3ds +
            0.15 * evidence_completeness
        )
        
        features = np.array([[
            amount, customer_tenure, prior_disputes, customer_risk/100,
            merchant_chargeback_rate/100, merchant_volume,
            is_cross_border, is_digital_goods, days_to_dispute,
            delivery_tracking, delivery_confirmation, avs_match,
            cvv_match, auth_3ds, evidence_completeness,
            evidence_score, is_repeat_disputer
        ]])
        
        features_scaled = scaler.transform(features)
        risk_score = model.predict_proba(features_scaled)[0][1]
        
        st.divider()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Risk Score", f"{risk_score:.2%}", 
                     delta="HIGH RISK" if risk_score >= threshold else "LOW RISK",
                     delta_color="inverse" if risk_score >= threshold else "normal")
        
        with col2:
            recommendation = "⚡ REPRESENT" if risk_score >= threshold else "✅ REFUND"
            st.metric("Recommendation", recommendation)
        
        with col3:
            evidence_display = f"{evidence_score:.1%}"
            st.metric("Evidence Strength", evidence_display)
        
        st.subheader("📋 Key Risk Factors")
        
        feature_importance = model.feature_importances_
        importance_df = pd.DataFrame({
            'Feature': FEATURES,
            'Importance': feature_importance
        }).sort_values('Importance', ascending=False).head(10)
        
        fig = px.bar(importance_df, x='Importance', y='Feature', orientation='h', title='Top 10 Feature Influences')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("💡 Action Advice")
        if risk_score >= threshold:
            st.warning(f"""
            **RECOMMENDATION: REPRESENT**
            
            - Evidence score is high enough to fight this chargeback
            - Gather delivery confirmation, AVS/CVV matches
            - Prepare representment package with all documentation
            - Estimated win probability: {(1-risk_score)*100:.1f}%
            """)
        else:
            st.success("""
            **RECOMMENDATION: REFUND**
            
            - Low fraud risk detected
            - Processing refund will save representment costs
            - Good customer experience outweighs fighting this case
            """)
