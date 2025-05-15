
# 🔍 PySpark Nginx Access Log Analysis

A PySpark-based analytics project to parse, analyze, and visualize Nginx access logs. This project is ideal for showcasing data engineering skills including log parsing, Spark transformations, data export, and Docker deployment.

---

## 📦 Features

- Parses raw Nginx access logs using regex
- Extracts:
  - IP address
  - Timestamp
  - HTTP method
  - Resource
  - Response code
  - Response size
- Analyzes:
  - Response code distribution
  - Traffic trends over time
  - Error rate
  - Top client/server errors
  - Redirect patterns
  - Top IP addresses and endpoints
  - HTTP method usage
- Exports results as CSV
- Optional Dockerized deployment

---

## 🛠️ Tech Stack

- Python 3
- Apache Spark (PySpark)
- Docker & Docker Compose (optional)
- Jupyter Notebook (optional for plotting)

---

## 📁 Project Structure

```
pyspark-access-log-analysis/
├── access.log                  # Sample Nginx access log
├── log_analysis.py            # Main PySpark script
├── output/                    # Directory for CSV outputs
├── Dockerfile                 # Dockerfile for PySpark container
├── docker-compose.yml         # Docker Compose configuration
├── requirements.txt           # Python dependencies
└── README.md                  # You're here
```

---

## ⚙️ Setup Instructions

## get nginx sample log

https://www.kaggle.com/datasets/eliasdabbas/web-server-access-logs

### 1. Clone the Repository

```bash
git clone https://github.com/manicn-daniel/nginx_access_log_analysis.git
cd pyspark-access-log-analysis
```

### 2. Install Dependencies (Locally)

```bash
pip install -r requirements.txt
```

### 3. Run the Analysis

Ensure your `access.log` is placed at the correct path (or update it in `log_analysis.py`).

```bash
python log_analysis.py
```

### 4. View Outputs

All result DataFrames will be saved as CSV in the `output/` directory.

---

## 📦 Run Using Docker (Optional)

### 1. Build and Run

```bash
docker-compose up --build
```

### 2. Stop the Container

```bash
docker-compose down
```

---

## 📊 Optional Jupyter Visualization

To generate plots:

1. Run a Jupyter notebook with `pandas` + `matplotlib`
2. Load CSVs from `output/`
3. Plot traffic, response code distribution, top endpoints, etc.

---

## ✅ Example Metrics Output

- Error Rate: `12.4%`
- Top 10 IPs:
  ```
  192.168.1.1 - 134 requests
  10.0.0.5 - 122 requests
  ...
  ```

---

## 🧑‍💻 Author

**Manic Daniel M**  
🗓️ Date: 24.12.2024  
📘 Purpose: Portfolio-worthy PySpark project for log analytics & data engineering

---

## 📜 License

MIT License — feel free to use, modify, and share.
