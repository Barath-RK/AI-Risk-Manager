import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import xgboost as xgb
import joblib
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("CHARGEBACK RISK SCORER - MODEL TRAINING")
print("="*60)

# Load data
print("\n1. Loading data...")
df = pd.read_csv('data/chargeback_cases_processed.csv')
print(f"   Shape: {df.shape}")

# Define features
features = [
    'transaction_amount',
    'customer_tenure_months',
    'customer_prior_disputes',
    'customer_risk_score',
    'merchant_chargeback_rate',
    'merchant_monthly_volume',
    'is_cross_border',
    'is_digital_goods',
    'days_to_dispute',
    'has_delivery_tracking',
    'has_delivery_confirmation',
    'has_avs_match',
    'has_cvv_match',
    'has_3ds_authentication',
    'evidence_completeness',
    'evidence_score',
    'is_repeat_disputer'
]

X = df[features]
y = df['representment_won']

print(f"   Features: {len(features)}")
print(f"   Target distribution: {y.value_counts().to_dict()}")

# Train-test split
print("\n2. Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"   Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")

# Scale features
print("\n3. Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
joblib.dump(scaler, 'models/scaler.pkl')
print("   Scaler saved!")

# Cost-sensitive XGBoost
print("\n4. Training cost-sensitive XGBoost...")

# Define costs
FN_COST = 550
FP_COST = 100

# Calculate scale_pos_weight
fraud_ratio = y_train.value_counts()[0] / y_train.value_counts()[1]
scale_weight = fraud_ratio * (FN_COST / FP_COST)
print(f"   Scale pos weight: {scale_weight:.2f}")

model = xgb.XGBClassifier(
    scale_pos_weight=scale_weight,
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric='logloss',
    use_label_encoder=False
)

model.fit(X_train_scaled, y_train, verbose=False)
print("   Model trained!")

# Predictions
print("\n5. Making predictions...")
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
y_pred = model.predict(X_test_scaled)

# Metrics
print("\n6. Model Performance:")
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred_proba)

print(f"   Precision: {precision:.4f}")
print(f"   Recall: {recall:.4f}")
print(f"   F1 Score: {f1:.4f}")
print(f"   ROC-AUC: {auc:.4f}")

# Confusion matrix
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
print(f"\n   Confusion Matrix:")
print(f"   TP: {tp}, FP: {fp}, FN: {fn}, TN: {tn}")

# Business cost analysis
print("\n7. Business Cost Analysis:")
total_cases = len(y_test)
if y_test.sum() > 0:
    actual_fraud_cases = y_test.sum()
else:
    actual_fraud_cases = 1

cost_no_model = actual_fraud_cases * FN_COST
print(f"   Cost with NO model: {cost_no_model:,} (approx)")

cost_with_model = (fp * FP_COST) + (fn * FN_COST)
savings = cost_no_model - cost_with_model
print(f"   Cost with model: {cost_with_model:,}")
print(f"   Net savings: {savings:,}")
print(f"   Savings %: {(savings/cost_no_model)*100:.1f}%")

# Find optimal threshold
print("\n8. Finding optimal threshold for business cost...")
thresholds = np.linspace(0.1, 0.9, 50)
best_threshold = 0.5
best_cost = float('inf')

for t in thresholds:
    preds = (y_pred_proba >= t).astype(int)
    fp_t = sum((preds == 1) & (y_test == 0))
    fn_t = sum((preds == 0) & (y_test == 1))
    cost_t = (fp_t * FP_COST) + (fn_t * FN_COST)
    if cost_t < best_cost:
        best_cost = cost_t
        best_threshold = t

print(f"   Optimal threshold: {best_threshold:.2f}")
print(f"   Minimum business cost: {best_cost:,}")

# Apply optimal threshold
optimal_preds = (y_pred_proba >= best_threshold).astype(int)
precision_opt = precision_score(y_test, optimal_preds)
recall_opt = recall_score(y_test, optimal_preds)
tn_opt, fp_opt, fn_opt, tp_opt = confusion_matrix(y_test, optimal_preds).ravel()

print(f"\n9. Performance at optimal threshold ({best_threshold:.2f}):")
print(f"   Precision: {precision_opt:.4f}")
print(f"   Recall: {recall_opt:.4f}")
print(f"   TP: {tp_opt}, FP: {fp_opt}, FN: {fn_opt}, TN: {tn_opt}")

# Save model and threshold
print("\n10. Saving model...")
joblib.dump(model, 'models/xgb_model.pkl')
joblib.dump(best_threshold, 'models/optimal_threshold.pkl')
print("   Model and threshold saved!")

# Save metrics for dashboard
metrics = {
    'precision': precision_opt,
    'recall': recall_opt,
    'auc': auc,
    'optimal_threshold': best_threshold,
    'fp_cost': FP_COST,
    'fn_cost': FN_COST,
    'savings': savings,
    'tp': int(tp_opt),
    'fp': int(fp_opt),
    'fn': int(fn_opt),
    'tn': int(tn_opt)
}
pd.DataFrame([metrics]).to_csv('models/metrics.csv', index=False)
print("   Metrics saved!")

print("\n" + "="*60)
print("✅ TRAINING COMPLETE!")
print("="*60)
