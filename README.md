# 🚀 Airflow-Orchestrated ETL Pipeline (REST API → CSV)

A simple, production-oriented (local) **ETL pipeline orchestrated with Apache Airflow**, demonstrating data ingestion, transformation, and basic data quality validation.

- **Extract** → fetches top 10 cryptocurrencies from CoinGecko (REST API)  
- **Transform** → cleans and normalizes data, adds extraction timestamp  
- **Load** → writes processed data to CSV (`data/processed_crypto_prices.csv`)  
- **Validate** → performs lightweight quality checks (row count, average price, top crypto)

---

## 🧩 Technology Stack

- **Apache Airflow 2.10** (Docker Compose, CeleryExecutor)  
- **Python 3.12**  
- **Pandas**, **Requests**  
- **Redis** + **PostgreSQL** (Airflow metastore)  
- **Docker Desktop**

---

## 📁 Project Structure

```text
airflow-crypto-etl/
├─ dags/
│  └─ crypto_etl_pipeline.py
├─ data/
│  ├─ raw/                  # created automatically
│  └─ processed_crypto_prices.csv
├─ logs/
├─ config/
├─ plugins/
└─ docker-compose.yaml
```

---

## ⚙️ Quick Start (Local)

1. **Set environment variables** (PowerShell):
   ```powershell
   $env:AIRFLOW_UID=50000
   $env:_PIP_ADDITIONAL_REQUIREMENTS="pandas requests"
   ```

2. **Initialize Airflow:**
   ```bash
   docker compose up airflow-init
   ```

3. **Start services:**
   ```bash
   docker compose up -d
   ```

4. **Open Airflow UI:**
   http://localhost:8080  
   Login: `airflow`  
   Password: `airflow`

5. **Enable and trigger the `crypto_etl_pipeline` DAG manually.**

---

## 🌐 API Details

**Endpoint:**  
https://api.coingecko.com/api/v3/coins/markets  

**Parameters:**  
- `vs_currency=usd`  
- `order=market_cap_desc`  
- `per_page=10`  
- `page=1`

---

## 📊 Output Data Schema

| column               | type      | description                     |
|----------------------|-----------|---------------------------------|
| crypto_id            | string    | Cryptocurrency ID               |
| symbol               | string    | Symbol (BTC, ETH, etc.)         |
| name                 | string    | Cryptocurrency name             |
| price_usd            | float     | Current price in USD            |
| market_cap           | float     | Market capitalization           |
| volume_24h           | float     | 24h trading volume              |
| price_change_24h_pct | float     | 24h price change percentage     |
| extracted_at         | timestamp | Data extraction timestamp       |

---

## 🧪 Data Validation

The `validate` task performs basic data quality checks and logs:
- number of rows  
- average USD price  
- name of the highest-priced cryptocurrency  

This step ensures pipeline correctness and basic data integrity.

---

## 🩺 Troubleshooting

❗ **Missing `data/` directory**  
Ensure the `data/` folder exists and is mounted in `x-airflow-common` within `docker-compose.yaml`.

⚙️ **DAG not visible in UI**  
Verify the DAG file is located in `/dags` and check if `DAGS_ARE_PAUSED_AT_CREATION=True` (manual enable required).

🐍 **Dependency issues**  
Check `_PIP_ADDITIONAL_REQUIREMENTS="pandas requests"` or build a custom Airflow image.

---

## 🗺️ Roadmap

> The roadmap reflects how this ETL pipeline could evolve into a cloud-native ELT architecture in a production environment.

- Write output data to **Parquet**  
- Data validation with **Great Expectations**  
- Hourly scheduling  
- Data sink to **S3 / BigQuery**  
- **Slack notifications** on DAG completion  

---

## 👨‍💻 Author

**Paweł Goleń** – Cloud Data Engineer  

Focus areas:
- ETL / data pipeline orchestration  
- Cloud data platforms (AWS, Azure)  
- Automation & data processing  

📎 LinkedIn: https://www.linkedin.com/in/pawel-golen/  
📦 GitHub: https://github.com/PawelGolen  

---

## 🧠 License

This project is released under the **MIT License**.
