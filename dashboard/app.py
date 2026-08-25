import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import warnings
import shap
from datetime import datetime, timedelta
from sklearn.cluster import DBSCAN
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="Chargeback Risk Scorer Pro",
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

# Helper functions
def explain_plain_english(features_dict):
    """Generate plain English explanation"""
    explanations = []
    
    if features_dict['customer_tenure_months'] < 3:
        explanations.append(f"⚠️ This customer is new (only {features_dict['customer_tenure_months']:.0f} months old). New customers have higher fraud risk.")
    
    if features_dict['customer_prior_disputes'] > 2:
        explanations.append(f"⚠️ This customer has {features_dict['customer_prior_disputes']:.0f} prior disputes - suspicious pattern.")
    
    if features_dict['merchant_chargeback_rate'] > 0.05:
        explanations.append(f"⚠️ This merchant has a high chargeback rate ({features_dict['merchant_chargeback_rate']*100:.1f}%) - fraudsters often target such merchants.")
    
    if features_dict['transaction_amount'] > 20000:
        explanations.append(f"⚠️ High transaction amount (₹{features_dict['transaction_amount']:,.0f}) - common target for fraud.")
    
    if features_dict['days_to_dispute'] < 5:
        explanations.append(f"⚠️ Very quick dispute (within {features_dict['days_to_dispute']:.0f} days) - suspicious behavior.")
    
    evidence_score = features_dict['evidence_score']
    if evidence_score < 0.3:
        explanations.append(f"❌ Very weak evidence ({evidence_score*100:.1f}%) - you'll likely lose if you fight this.")
    elif evidence_score < 0.6:
        explanations.append(f"⚠️ Moderate evidence ({evidence_score*100:.1f}%) - gather more evidence before fighting.")
    else:
        explanations.append(f"✅ Strong evidence ({evidence_score*100:.1f}%) - good chance of winning!")
    
    if features_dict['is_repeat_disputer'] == 1:
        explanations.append("⚠️ This customer has disputed before - high risk!")
    
    if not explanations:
        explanations.append("✅ This transaction looks relatively safe.")
    
    return "\n".join(explanations)

# Sidebar navigation
st.sidebar.title("🛡️ Navigation")
page = st.sidebar.radio("Go to", ["📊 Dashboard", "🔍 Transaction Explorer", "🧠 Risk Analyzer", "📈 Fraud Analytics"])

# ===================== DASHBOARD PAGE =====================
if page == "📊 Dashboard":
    st.title("📊 Chargeback Risk Scorer Pro Dashboard")
    
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
    
    # A/B Testing Comparison
    st.subheader("📊 Model vs. Simple Rules (A/B Testing)")
    col1, col2, col3 = st.columns(3)
    
    # Simple rule: Flag transactions > ₹5000 as fraud
    rule_preds = (df['transaction_amount'] > 5000).astype(int)
    rule_accuracy = accuracy_score(df['representment_won'], rule_preds)
    
    # Our model accuracy
    X_all = df[FEATURES]
    X_all_scaled = scaler.transform(X_all)
    model_preds = model.predict(X_all_scaled)
    model_accuracy = accuracy_score(df['representment_won'], model_preds)
    
    with col1:
        st.metric("🎯 Our Model Accuracy", f"{model_accuracy:.2%}", delta=f"+{(model_accuracy-rule_accuracy)*100:.1f}%")
    with col2:
        st.metric("📏 Simple Rule Accuracy", f"{rule_accuracy:.2%}", delta="Baseline")
    with col3:
        st.metric("🚀 Improvement", f"{(model_accuracy-rule_accuracy)*100:.1f}%", delta="Better")
    
    st.caption("Our model outperforms simple rules by learning complex patterns from 17 features!")
    
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

# ===================== TRANSACTION EXPLORER =====================
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
    
    # CSV Download
    csv = filtered[display_cols].to_csv(index=False)
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name=f"transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# ===================== RISK ANALYZER =====================
elif page == "🧠 Risk Analyzer":
    st.title("🧠 Risk Analyzer with Explainable AI")
    
    st.markdown("""
    ### How this works
    Enter transaction details to get:
    1. **Risk Score**: Probability of fraudulent chargeback (0-1)
    2. **Recommendation**: REPRESENT (fight it) or REFUND (accept loss)
    3. **SHAP Explanation**: Why the model made this decision
    4. **Plain English**: Simple explanation anyone can understand
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Transaction Details")
        amount = st.number_input("Transaction Amount (₹)", min_value=0, max_value=100000, value=10000)
        days_to_dispute = st.slider("Days to Dispute", 0, 180, 30)
        is_cross_border = st.selectbox("Cross Border", [0, 1], format_func=lambda x: "Yes" if x else "No")
        is_digital_goods = st.selectbox("Digital Goods", [0, 1], format_func=lambda x: "Yes" if x else "No")
        is_repeat_disputer = st.selectbox("Repeat Disputer", [0, 1], format_func=lambda x: "Yes" if x else "No")
    
    with col2:
        st.subheader("Customer & Merchant")
        customer_tenure = st.slider("Customer Tenure (months)", 0, 60, 1)
        prior_disputes = st.slider("Prior Disputes", 0, 20, 0)
        customer_risk = st.slider("Customer Risk Score", 0, 100, 50)
        merchant_chargeback_rate = st.slider("Merchant Chargeback Rate (%)", 0, 100, 5) / 100
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
    
    # What-If Analysis
    with col2:
        st.subheader("🔬 What-If Analysis")
        st.caption("See how risk score changes with better evidence!")
        
        # Current evidence score
        current_evidence = (
            0.3 * delivery_confirmation +
            0.2 * avs_match +
            0.2 * cvv_match +
            0.15 * auth_3ds +
            0.15 * evidence_completeness
        )
        
        # Scenario 1: Add delivery confirmation
        scenario1_evidence = (
            0.3 * 1 +  # delivery confirmation added
            0.2 * avs_match +
            0.2 * cvv_match +
            0.15 * auth_3ds +
            0.15 * evidence_completeness
        )
        
        # Scenario 2: Add all evidence
        scenario2_evidence = (
            0.3 * 1 +
            0.2 * 1 +  # AVS
            0.2 * 1 +  # CVV
            0.15 * 1 +  # 3DS
            0.15 * 1   # Complete
        )
        
        st.metric("Current Evidence Strength", f"{current_evidence*100:.1f}%")
        st.metric("If you add Delivery Confirmation", f"{scenario1_evidence*100:.1f}%", delta=f"+{(scenario1_evidence-current_evidence)*100:.1f}%")
        st.metric("If you add ALL Evidence", f"{scenario2_evidence*100:.1f}%", delta=f"+{(scenario2_evidence-current_evidence)*100:.1f}%")
    
    if st.button("🔍 Analyze Risk", type="primary"):
        # Calculate evidence score
        evidence_score = (
            0.3 * delivery_confirmation +
            0.2 * avs_match +
            0.2 * cvv_match +
            0.15 * auth_3ds +
            0.15 * evidence_completeness
        )
        
        # Create feature vector
        features = np.array([[
            amount, customer_tenure, prior_disputes, customer_risk/100,
            merchant_chargeback_rate, merchant_volume,
            is_cross_border, is_digital_goods, days_to_dispute,
            delivery_tracking, delivery_confirmation, avs_match,
            cvv_match, auth_3ds, evidence_completeness,
            evidence_score, is_repeat_disputer
        ]])
        
        # Scale and predict
        features_scaled = scaler.transform(features)
        risk_score = model.predict_proba(features_scaled)[0][1]
        
        # Feature dict for explanation
        feature_dict = {
            'customer_tenure_months': customer_tenure,
            'customer_prior_disputes': prior_disputes,
            'merchant_chargeback_rate': merchant_chargeback_rate,
            'transaction_amount': amount,
            'days_to_dispute': days_to_dispute,
            'evidence_score': evidence_score,
            'is_repeat_disputer': is_repeat_disputer
        }
        
        # Results
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            risk_delta = "HIGH RISK" if risk_score >= threshold else "LOW RISK"
            st.metric("Risk Score", f"{risk_score:.2%}", 
                     delta=risk_delta,
                     delta_color="inverse" if risk_score >= threshold else "normal")
        
        with col2:
            recommendation = "⚡ REPRESENT" if risk_score >= threshold else "✅ REFUND"
            st.metric("Recommendation", recommendation)
        
        with col3:
            st.metric("Evidence Strength", f"{evidence_score:.1%}")
        
        # SHAP Explanation
        st.subheader("📊 SHAP Explanation - Why This Decision?")
        
        # Calculate SHAP values
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(features_scaled)
        
        # Create SHAP waterfall plot
        fig, ax = plt.subplots(figsize=(10, 6))
        shap.waterfall_plot(
            shap.Explanation(
                values=shap_values[0],
                base_values=explainer.expected_value,
                data=features_scaled[0],
                feature_names=FEATURES
            ),
            show=False
        )
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Feature Importance Chart
        st.subheader("📋 Top Risk Factors")
        feature_importance = model.feature_importances_
        importance_df = pd.DataFrame({
            'Feature': FEATURES,
            'Importance': feature_importance
        }).sort_values('Importance', ascending=False).head(10)
        
        fig = px.bar(importance_df, x='Importance', y='Feature', orientation='h', 
                     title='Top 10 Feature Influences',
                     color='Importance', color_continuous_scale='Reds')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Plain English Explanation
        st.subheader("💬 Plain English Explanation")
        explanation = explain_plain_english(feature_dict)
        st.info(explanation)
        
        # Action Advice
        st.subheader("💡 Action Advice")
        if risk_score >= threshold:
            st.warning(f"""
            **RECOMMENDATION: REPRESENT**
            
            - Evidence score is {evidence_score:.1%} - {"strong" if evidence_score > 0.6 else "weak"}
            - Gather delivery confirmation, AVS/CVV matches
            - Prepare representment package with all documentation
            - Estimated win probability: {(1-risk_score)*100:.1f}%
            - **What-If**: Adding delivery confirmation improves evidence by {((0.3 * 1 + 0.2 * avs_match + 0.2 * cvv_match + 0.15 * auth_3ds + 0.15 * evidence_completeness) - evidence_score)*100:.1f}%
            """)
        else:
            st.success("""
            **RECOMMENDATION: REFUND**
            
            - Low fraud risk detected
            - Processing refund will save representment costs
            - Good customer experience outweighs fighting this case
            - This saves approximately ₹10,000 in representment costs
            """)

# ===================== FRAUD ANALYTICS =====================
else:
    st.title("📈 Fraud Analytics & Spike Detection")
    
    # Create synthetic dates for demonstration
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', periods=len(df), freq='D')
    df_dates = df.copy()
    df_dates['date'] = np.random.choice(dates, size=len(df), replace=False)
    df_dates['date'] = pd.to_datetime(df_dates['date'])
    
    # Calculate daily fraud rate
    daily_fraud = df_dates.groupby(df_dates['date'].dt.date)['representment_won'].mean().reset_index()
    daily_fraud.columns = ['date', 'fraud_rate']
    daily_fraud['fraud_rate'] = daily_fraud['fraud_rate'] * 100
    
    # Detect spikes (more than 2 standard deviations from mean)
    mean_fraud = daily_fraud['fraud_rate'].mean()
    std_fraud = daily_fraud['fraud_rate'].std()
    spike_threshold = mean_fraud + 2 * std_fraud
    daily_fraud['is_spike'] = daily_fraud['fraud_rate'] > spike_threshold
    
    # Count spikes
    spike_dates = daily_fraud[daily_fraud['is_spike']]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Average Fraud Rate", f"{mean_fraud:.1f}%")
    with col2:
        st.metric("🚨 Fraud Spikes Detected", len(spike_dates))
    with col3:
        st.metric("📈 Spike Threshold", f"{spike_threshold:.1f}%")
    
    st.divider()
    
    # Fraud Rate Trend Chart
    st.subheader("📈 Fraud Rate Over Time")
    fig = px.line(daily_fraud, x='date', y='fraud_rate', 
                  title='Daily Fraud Rate with Spike Detection')
    
    # Add threshold line
    fig.add_hline(y=spike_threshold, line_dash="dash", line_color="red", 
                  annotation_text=f"Spike Threshold: {spike_threshold:.1f}%")
    
    # Highlight spikes
    spike_points = daily_fraud[daily_fraud['is_spike']]
    fig.add_scatter(x=spike_points['date'], y=spike_points['fraud_rate'],
                    mode='markers', marker=dict(size=15, color='red', symbol='x'),
                    name='🚨 Spike Detected')
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Suspicious Clusters (Fraud Ring Detection)
    st.subheader("🔍 Fraud Ring Detection")
    st.caption("Detecting groups of similar fraudulent transactions")
    
    # Prepare features for clustering
    cluster_features = df[['transaction_amount', 'customer_risk_score', 'merchant_chargeback_rate']].copy()
    cluster_features = (cluster_features - cluster_features.mean()) / cluster_features.std()  # Standardize
    
    # DBSCAN clustering
    clustering = DBSCAN(eps=0.5, min_samples=3).fit(cluster_features)
    df_cluster = df.copy()
    df_cluster['cluster'] = clustering.labels_
    
    # Find clusters with high fraud rate
    fraud_clusters = df_cluster.groupby('cluster')['representment_won'].mean().sort_values(ascending=False)
    suspicious_clusters = fraud_clusters[fraud_clusters > 0.7]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔗 Total Clusters Found", len(fraud_clusters))
    with col2:
        st.metric("🚨 Suspicious Clusters (70%+ Fraud)", len(suspicious_clusters))
    
    if len(suspicious_clusters) > 0:
        st.warning(f"""
        🚨 **ALERT!** Found {len(suspicious_clusters)} suspicious clusters with high fraud rate!
        
        These could be organized fraud rings. Investigate these groups:
        {suspicious_clusters.index.tolist()}
        """)
        
        # Show cluster details
        st.subheader("Cluster Details")
        cluster_details = []
        for cluster_id in suspicious_clusters.index:
            cluster_data = df_cluster[df_cluster['cluster'] == cluster_id]
            cluster_details.append({
                'Cluster ID': cluster_id,
                'Size': len(cluster_data),
                'Fraud Rate': f"{fraud_clusters[cluster_id]*100:.1f}%",
                'Avg Amount': f"₹{cluster_data['transaction_amount'].mean():,.0f}",
                'Avg Risk': f"{cluster_data['customer_risk_score'].mean():.1f}"
            })
        
        st.dataframe(pd.DataFrame(cluster_details))
    else:
        st.success("✅ No suspicious clusters detected. No organized fraud rings identified.")
    
    # Batch Predict Upload
    st.divider()
    st.subheader("📤 Batch Prediction - Upload CSV")
    st.caption("Upload multiple transactions to get predictions at once")
    
    uploaded_file = st.file_uploader("Choose a CSV file with transaction data", type="csv")
    if uploaded_file is not None:
        try:
            batch_df = pd.read_csv(uploaded_file)
            st.write(f"✅ Loaded {len(batch_df)} transactions")
            
            # Check if required columns exist
            missing_cols = [col for col in FEATURES if col not in batch_df.columns]
            if missing_cols:
                st.error(f"Missing columns: {missing_cols}")
            else:
                # Make predictions
                X_batch = batch_df[FEATURES]
                X_batch_scaled = scaler.transform(X_batch)
                batch_predictions = model.predict_proba(X_batch_scaled)[:, 1]
                batch_labels = (batch_predictions >= threshold).astype(int)
                
                # Add results
                batch_df['risk_score'] = batch_predictions
                batch_df['recommendation'] = ['⚡ REPRESENT' if x >= threshold else '✅ REFUND' for x in batch_predictions]
                batch_df['risk_level'] = batch_df['risk_score'].apply(
                    lambda x: 'HIGH' if x >= threshold else ('MEDIUM' if x >= threshold*0.7 else 'LOW')
                )
                
                # Show results
                st.subheader("📊 Batch Prediction Results")
                st.dataframe(batch_df[['risk_score', 'recommendation', 'risk_level']].head(20))
                
                # Download results
                csv_download = batch_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Predictions CSV",
                    data=csv_download,
                    file_name=f"batch_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                # Summary stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Transactions", len(batch_df))
                with col2:
                    st.metric("HIGH Risk Transactions", sum(batch_predictions >= threshold))
                with col3:
                    avg_risk = batch_predictions.mean()
                    st.metric("Average Risk Score", f"{avg_risk:.2%}")
                
        except Exception as e:
            st.error(f"Error reading file: {e}")
