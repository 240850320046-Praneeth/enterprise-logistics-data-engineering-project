# File Source Design

## 1. Purpose

The Warehouse Management System provides package processing and dispatch information through files.

The logistics platform will support both CSV and JSON files as batch data sources.

These files simulate data received from warehouses during normal business operations.

---

# 2. Source System

Source System:

Warehouse Management System

Data Type:

Package and warehouse operational data

Processing Type:

Batch

File Formats:

- CSV
- JSON

Expected Frequency:

- Hourly
- Daily

---

# 3. CSV File Structure

Example CSV:

```text
warehouse_id,package_id,order_id,package_weight,processing_time,dispatch_time
WH001,PK10001,ORD10001,4.5,22,2026-08-19T10:30:00
WH002,PK10002,ORD10002,2.8,15,2026-08-19T10:35:00
WH001,PK10003,ORD10003,7.2,30,2026-08-19T10:40:00