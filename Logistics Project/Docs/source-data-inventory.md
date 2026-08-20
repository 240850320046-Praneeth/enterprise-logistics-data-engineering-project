# Source Data Inventory

## Project

Enterprise Logistics Data Engineering Project

## Source Systems

### 1. SQL Server

Database: `LogisticsDB`

| Table             | Records | Source Type         |
| ----------------- | ------: | ------------------- |
| customers         |     500 | Master Data         |
| deliveries        |   2,500 | Transactional Data  |
| drivers           |      50 | Master Data         |
| orders            |   2,000 | Transactional Data  |
| pipeline_audit    |       0 | Pipeline Metadata   |
| vehicle_locations |   1,000 | Event/Location Data |
| vehicles          |      75 | Master Data         |
| warehouses        |      10 | Master Data         |

### 2. CSV File Source

| File                | Records | Description                 |
| ------------------- | ------: | --------------------------- |
| daily_orders        |     100 | External partner order data |
| warehouse_inventory |      50 | Warehouse inventory data    |

### 3. API Source

| Source          | Records | Format |
| --------------- | ------: | ------ |
| delivery_events |     100 | JSON   |

This currently simulates an external delivery API response.

### 4. IoT Source

| Source                | Records | Format |
| --------------------- | ------: | ------ |
| vehicle_sensor_events |     100 | JSON   |

The data contains vehicle sensor information such as location, speed, fuel level, engine temperature, and vehicle status.

### 5. Application Log Source

| Source                |           Records | Format |
| --------------------- | ----------------: | ------ |
| logistics_application | Approximately 100 | Log    |

The application logs contain INFO, WARNING, and ERROR events.

## Source Architecture

```text
SQL Server ────────────┐
CSV Files ─────────────┤
API JSON ──────────────┼──> Enterprise Data Sources
IoT Events ────────────┤
Application Logs ──────┘
```

## Next Phase

The next phase is to ingest these source systems into Azure Data Lake Storage Gen2 using appropriate ingestion mechanisms.
