import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import time

# ── CONFIG ──────────────────────────────────────────────────
load_dotenv()

DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST     = os.getenv("DB_HOST")
DB_PORT     = int(os.getenv("DB_PORT", 3306))
DB_NAME     = "fraud_detection"
# ────────────────────────────────────────────────────────────

def create_db(engine_base):
    with engine_base.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        conn.commit()
    print(f"  ✅ Database '{DB_NAME}' ready.")

def load_transactions(engine):
    print("Loading scored_transactions...")
    df = pd.read_csv("data/scored_transactions.csv")
    print(f"  Rows: {len(df):,}")

    risk_order_map = {'Critical': 1, 'High': 2, 'Medium': 3, 'Low': 4}
    df['risk_order'] = df['risk_level'].map(risk_order_map)

    t0 = time.time()
    df.to_sql("transactions", con=engine, if_exists="replace",
              index=False, chunksize=5000, method="multi")
    print(f"  Loaded in {time.time()-t0:.1f}s")

    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE transactions ADD INDEX idx_fraud (is_fraud)"))
        conn.execute(text("ALTER TABLE transactions ADD INDEX idx_risk (risk_level(20))"))
        conn.execute(text("ALTER TABLE transactions ADD INDEX idx_score (fraud_score)"))
        conn.commit()
    print("  Indexes created.")

def load_model_metrics(engine):
    print("Loading model_metrics...")
    metrics = pd.DataFrame([
        {
            'model': 'Logistic Regression',
            'auc_roc': 0.9697, 'avg_precision': 0.7148,
            'recall': 0.9082, 'precision': 0.0651, 'f1': 0.1214
        },
        {
            'model': 'Random Forest',
            'auc_roc': 0.9823, 'avg_precision': 0.7891,
            'recall': 0.8776, 'precision': 0.3346, 'f1': 0.4845
        },
        {
            'model': 'XGBoost',
            'auc_roc': 0.9759, 'avg_precision': 0.8240,
            'recall': 0.8469, 'precision': 0.4110, 'f1': 0.5533
        }
    ])
    metrics.to_sql("model_metrics", con=engine, if_exists="replace", index=False)
    print(f"  ✅ model_metrics: {len(metrics)} rows")

def load_business_impact(engine):
    print("Loading business_impact...")
    impact = pd.DataFrame([
        {'metric': 'Total Transactions',  'value': 284807},
        {'metric': 'Real Fraud Cases',    'value': 492},
        {'metric': 'Fraud Detected',      'value': 477},
        {'metric': 'False Alarms',        'value': 292},
        {'metric': 'Fraud Missed',        'value': 15},
        {'metric': 'Fraud Prevented ($)', 'value': 58295},
        {'metric': 'Review Cost ($)',     'value': 1460},
        {'metric': 'Fraud Missed ($)',    'value': 1833},
        {'metric': 'Net Benefit ($)',     'value': 55002},
    ])
    impact.to_sql("business_impact", con=engine, if_exists="replace", index=False)
    print(f"  ✅ business_impact: {len(impact)} rows")

def verify(engine):
    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM transactions")).scalar()
        fraud = conn.execute(text("SELECT COUNT(*) FROM transactions WHERE is_fraud = 1")).scalar()
        risk  = conn.execute(text("""
            SELECT risk_level, COUNT(*) as cnt,
                   ROUND(AVG(fraud_score), 4) as avg_score
            FROM transactions
            GROUP BY risk_level
            ORDER BY avg_score DESC
        """)).fetchall()

    print(f"\n✅ Verification:")
    print(f"   Total transactions : {total:,}")
    print(f"   Fraud cases        : {fraud:,} ({fraud/total*100:.3f}%)")
    print(f"\n   {'Risk Level':<12} {'Count':>8} {'Avg Score':>10}")
    print(f"   {'─'*32}")
    for row in risk:
        print(f"   {row[0]:<12} {row[1]:>8,} {row[2]:>10.4f}")

if __name__ == "__main__":
    base_engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
    )
    create_db(base_engine)

    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    load_transactions(engine)
    load_model_metrics(engine)
    load_business_impact(engine)
    verify(engine)

    print("\n✅ Pipeline complete. Ready to connect from Power BI.")