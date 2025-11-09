# 🚀 Airflow Crypto ETL (CoinGecko → CSV)

Prosty, produkcyjnie “przyjazny” (lokalnie) pipeline ETL w **Apache Airflow**:
- **Extract** → pobiera top 10 kryptowalut z CoinGecko (REST API)
- **Transform** → czyści / normalizuje dane i dodaje timestamp
- **Load** → zapisuje dane do CSV w folderze `data/processed_crypto_prices.csv`
- **Validate** → szybki quality check (liczba wierszy, średnia ceny, top crypto)

---

## 🧩 Stack technologiczny

- **Apache Airflow 2.10** (Docker Compose, CeleryExecutor)
- **Python 3.12**
- **Pandas**, **Requests**
- **Redis** + **Postgres** (Airflow metastore)
- **Docker Desktop**

---

## 📁 Struktura projektu

airflow-crypto-etl/
├─ dags/
│ └─ crypto_etl_pipeline.py
├─ data/
│ ├─ raw/ (tworzone automatycznie)
│ └─ processed_crypto_prices.csv
├─ logs/
├─ config/
├─ plugins/
└─ docker-compose.yaml

---

## ⚙️ Szybki start (lokalnie)

1. **Ustaw zmienne środowiskowe** (PowerShell):
   $env:AIRFLOW_UID=50000
   $env:_PIP_ADDITIONAL_REQUIREMENTS="pandas requests"

2. **Zainicjuj Airflow:**
   docker compose up airflow-init

3. **Uruchom klastry:**
   docker compose up -d

4. **Otwórz UI:**
   http://localhost:8080  
   Login: airflow  
   Hasło: airflow

5. **Włącz DAG crypto_etl_pipeline i uruchom ręcznie (Trigger).**

---

🌐 Parametry API  
Endpoint: https://api.coingecko.com/api/v3/coins/markets  
Params: vs_currency=usd, order=market_cap_desc, per_page=10, page=1

---

📊 Schemat danych (wynik)

| column               | type      | description             |
| -------------------- | --------- | ----------------------- |
| crypto_id            | string    | ID kryptowaluty         |
| symbol               | string    | Symbol (BTC, ETH, itp.) |
| name                 | string    | Nazwa kryptowaluty      |
| price_usd            | float     | Aktualna cena w USD     |
| market_cap           | float     | Kapitalizacja rynkowa   |
| volume_24h           | float     | Wolumen handlu 24h      |
| price_change_24h_pct | float     | Zmiana ceny w %         |
| extracted_at         | timestamp | Data pobrania           |

---

🧪 Walidacja danych  
Operator validate sprawdza poprawność danych i loguje m.in.:  
- liczbę wierszy (rows)  
- średnią cenę USD (avg_price_usd)  
- nazwę najdroższej kryptowaluty (top_crypto)

---

🩺 Troubleshooting  
❗ Brak katalogu data → upewnij się, że folder data/ istnieje i jest zamontowany w x-airflow-common w docker-compose.yaml.  
⚙️ DAG niewidoczny w UI → sprawdź, czy plik znajduje się w /dags i czy DAGS_ARE_PAUSED_AT_CREATION=True (wtedy trzeba go ręcznie włączyć).  
🐍 Błędy zależności → sprawdź _PIP_ADDITIONAL_REQUIREMENTS="pandas requests" lub zbuduj własny image Airflow.

---

🗺️ Roadmap  
- Zapis do Parquet  
- Walidacja z Great Expectations  
- Harmonogram co 1h  
- Sink danych do S3 / BigQuery  
- Slack alerty po zakończeniu DAG-a  

---

👨‍💻 Autor  
Paweł Goleń  
Cloud / Data Engineer @ Deloitte  
AWS | Azure | ETL | AI & Automation  

📎 LinkedIn  https://www.linkedin.com/in/pawel-golen/
📦 GitHub  https://github.com/PawelGolen

---

🧠 Licencja  
Projekt dostępny na licencji MIT.
