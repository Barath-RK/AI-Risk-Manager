# Data Exploration Script
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("="*50)
print("LOADING DATA")
print("="*50)

df = pd.read_csv('data/chargeback_cases.csv')
print(f"Shape: {df.shape}")
print(f"\nColumns:\n{df.columns.tolist()}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nData types:\n{df.dtypes}")

print("\n" + "="*50)
print("TARGET VARIABLE ANALYSIS")
print("="*50)

print(f"Target distribution:\n{df['representment_won'].value_counts()}")
print(f"Target distribution (%):\n{df['representment_won'].value_counts(normalize=True)}")

# Check for missing values
print("\n" + "="*50)
print("MISSING VALUES")
print("="*50)
print(df.isnull().sum().sort_values(ascending=False).head(20))

# Correlation with target
print("\n" + "="*50)
print("TOP CORRELATIONS WITH TARGET")
print("="*50)

numeric_cols = df.select_dtypes(include=[np.number]).columns
correlation = df[numeric_cols].corr()['representment_won'].sort_values(ascending=False)
print(correlation.head(20))

# Create evidence_score composite
print("\n" + "="*50)
print("CREATING EVIDENCE SCORE")
print("="*50)

evidence_features = ['has_delivery_tracking', 'has_delivery_confirmation', 
                     'has_avs_match', 'has_cvv_match', 'has_3ds_authentication',
                     'evidence_completeness']
df['evidence_score'] = (
    0.3 * df['has_delivery_confirmation'] +
    0.2 * df['has_avs_match'] +
    0.2 * df['has_cvv_match'] +
    0.15 * df['has_3ds_authentication'] +
    0.15 * df['evidence_completeness']
)

print(f"Evidence Score - Min: {df['evidence_score'].min():.2f}, Max: {df['evidence_score'].max():.2f}, Mean: {df['evidence_score'].mean():.2f}")

# Save processed data
df.to_csv('data/chargeback_cases_processed.csv', index=False)
print("\n✅ Processed data saved!")

# Summary statistics by target
print("\n" + "="*50)
print("SUMMARY BY TARGET")
print("="*50)

print(df.groupby('representment_won')[['transaction_amount', 'customer_tenure_months', 
                                       'customer_prior_disputes', 'evidence_score']].mean())

print("\n✅ Exploration complete!")
