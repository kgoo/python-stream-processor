\# Python Stream Processor with Faust, Kafka, Postgres, and Grafana

This project demonstrates a lightweight Kafka stream processor using [Faust](https://faust-streaming.readthedocs.io/) to consume event messages, aggregate them in time windows, and store the results in PostgreSQL. Grafana is used to visualize the data.

---

\## 🔧 Features

- Reads key/value events from a Kafka topic  
- Aggregates counts of events by `value` every 10 seconds  
- Stores the results to a PostgreSQL table  
- Visualizes aggregated results in Grafana  

---

\## 🐳 Getting Started with Docker Compose

\### 1. Clone the repository

\`\`\`bash
git clone https://github.com/your-username/python-stream-processor.git
cd python-stream-processor
\`\`\`

\### 2. Create a `.env` file

\`\`\`ini
\# .env
POSTGRES_USER=faustuser
POSTGRES_PASSWORD=faustpass
POSTGRES_DB=faustdb
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin
\`\`\`

\### 3. Start services (Postgres + Grafana)

\`\`\`bash
docker-compose up -d
\`\`\`

Postgres: `localhost:5432`  
Grafana: `http://localhost:3000` (login using the credentials from `.env`)

Grafana will automatically connect to the Postgres DB and use the preconfigured dashboard.

---

\## 🚀 Running the Faust Stream Processor

\### 1. Activate the virtual environment

\`\`\`bash
python -m venv .venv
source .venv/bin/activate  \# On Windows: .venv\Scripts\activate
\`\`\`

\### 2. Install dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

\### 3. Start the Faust worker

\`\`\`bash
faust -A stream_app worker -l info
\`\`\`

You should see log messages like `Received event:` and `store_aggregate:` once Kafka messages are consumed and written to Postgres.

---

\## 📤 Producing Sample Events

Use any Kafka client or CLI to publish events to the `events` topic.

Example JSON:

\`\`\`json
{
  "key": "some_key",
  "value": "some_val1",
  "timestamp": 1744556173857
}
\`\`\`

---

\## 📈 Viewing in Grafana

- Open [http://localhost:3000](http://localhost:3000)  
- Login with admin credentials  
- Explore the preloaded dashboard showing value counts per window  

---

\## 🧹 Cleaning Up

To stop and remove containers **and volumes**:

\`\`\`bash
docker-compose down -v
\`\`\`

---

\## 📁 Project Structure

\`\`\`
.
├── docker-compose.yml
├── .env
├── init.sql
├── stream_app/
│   ├── \_\_init\_\_.py
│   ├── stream_app.py      \# Main Faust app
│   ├── db.py              \# SQLAlchemy connection + store_aggregate()
│   ├── models.py          \# Event & Aggregate models
└── grafana/
    └── provisioning/
        ├── datasources/
        └── dashboards/
\`\`\`

---

\## ✅ Notes

- Faust runs on Kafka and uses changelog topics automatically  
- Aggregations are done in tumbling 10s windows  
- Postgres stores window start timestamps in UTC  
