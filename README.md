# Python Stream Processor

This is a Faust-based Kafka stream processor that consumes JSON events, performs time-series aggregations on the `value` field, and stores the results in a PostgreSQL database. Grafana is used to visualize the data.

---

## 🔧 Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-user/python-stream-processor.git
cd python-stream-processor
```

### 2. Create a `.env` file
Create a `.env` file in the root directory:

```env
POSTGRES_USER=faustuser
POSTGRES_PASSWORD=faustpass
POSTGRES_DB=faustdb
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 3. Start Docker services (Postgres + Grafana)
```bash
docker compose up -d
```

This will:
- Start a Postgres database and Grafana container.
- Grafana will be accessible at: http://localhost:3000
- Default credentials:
  - **Username:** `admin`
  - **Password:** `admin`

A default dashboard will be auto-provisioned if configured in `grafana/provisioning`.

---

## 🚀 Running Faust

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the Faust worker:
```bash
faust -A stream_app worker -l info
```

Faust will:
- Connect to the `events` Kafka topic
- Aggregate event counts by `value`
- Store aggregated counts into the Postgres database every 10 seconds

---

## 📈 Viewing Data in Grafana

- Go to: [http://localhost:3000](http://localhost:3000)
- Log in with `admin` / `admin`
- Select the "Event Aggregates" dashboard
- View event counts grouped by `value` in real-time

---

## 🧪 Producing Events (Example)
Use any Kafka producer to publish JSON messages to the `events` topic.

Example message:
```json
{
  "key": "user123",
  "value": "click"
}
```

---

## 🧹 Clean up Docker (including volumes)

To stop everything and remove volumes:
```bash
docker compose down -v
```

---

## ✅ Notes

- Faust uses tumbling windows of 10 seconds and aggregates values by count.
- All data is written to PostgreSQL and visualized in Grafana.
- Timestamp windowing is in UTC.
