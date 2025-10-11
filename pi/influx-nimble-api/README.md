# InfluxQuickAPI

Minimal, memory-efficient Go API server to query InfluxDB v2.

## Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your InfluxDB details:
   ```
   INFLUXDB_URL=http://your-influxdb-host:8086
   INFLUXDB_TOKEN=your-token-here
   ```

3. Start the API:
   ```bash
   docker-compose up -d
   ```

## Usage

Query InfluxDB using a GET request:

```bash
curl "http://localhost:8080/query?org=YOUR_ORG&query=from(bucket:\"YOUR_BUCKET\")%20|>%20range(start:-1h)"
```

### Parameters:
- `org` - Your InfluxDB organization name
- `query` - Flux query string (URL-encoded)

### Example:

```bash
curl "http://localhost:8080/query?org=myorg&query=from(bucket:\"mybucket\")%20|>%20range(start:-5m)%20|>%20filter(fn:(r)%20=>%20r._measurement%20==%20\"temperature\")"
```

Response:
```json
{
  "data": [
    {
      "_time": "2025-10-10T12:00:00Z",
      "_value": 23.5,
      "_field": "value",
      "_measurement": "temperature"
    }
  ]
}
```

## Memory Limits

The container is limited to:
- 64MB RAM
- 0.5 CPU cores

Adjust in `docker-compose.yml` if needed.
