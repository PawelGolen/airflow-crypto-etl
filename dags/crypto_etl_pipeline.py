from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd, requests, json, logging
import os

default_args = {
    'owner': 'pawel_golen',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

log = logging.getLogger(__name__)
RAW = '/opt/airflow/data/raw_crypto_data.json'
CSV = '/opt/airflow/data/transformed_crypto_data.csv'
REP = '/opt/airflow/data/validation_report.json'

def extract(**_):
    os.makedirs(os.path.dirname(RAW), exist_ok=True)
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {'vs_currency':'usd','order':'market_cap_desc','per_page':10,'page':1}
    r = requests.get(url, params=params, timeout=15); r.raise_for_status()
    with open(RAW, 'w') as f: json.dump(r.json(), f)
    log.info("Extracted ok."); return 1

def transform(**_):
    data = json.load(open(RAW))
    df = pd.DataFrame(data)[['id','symbol','name','current_price','market_cap','total_volume','price_change_percentage_24h']]
    df.columns = ['crypto_id','symbol','name','price_usd','market_cap','volume_24h','price_change_24h_pct']
    df['extracted_at'] = datetime.now()
    df.to_csv(CSV, index=False); return len(df)

def validate(**_):
    df = pd.read_csv(CSV)
    rep = {'rows':len(df),'avg_price_usd':round(df['price_usd'].mean(),2),
           'top_crypto': (df.iloc[0]['name'] if len(df) else None),
           'timestamp': datetime.now().isoformat()}
    json.dump(rep, open(REP,'w'), indent=2)
    log.info(f"Validation: {rep}"); return rep

with DAG('crypto_etl_pipeline', default_args=default_args, schedule_interval='@daily',
         catchup=False, tags=['etl','crypto']) as dag:
    t1 = PythonOperator(task_id='extract', python_callable=extract)
    t2 = PythonOperator(task_id='transform', python_callable=transform)
    t3 = PythonOperator(task_id='validate', python_callable=validate)
    t1 >> t2 >> t3
