
---

# 3. `data-dictionary.md`

This will describe **what each important field means**.

Paste:

```markdown
# Data Dictionary

## 1. Purpose

This document defines the important entities and attributes used by the Logistics Data Platform.

---

# 2. Customer

| Column | Data Type | Description | Required |
|---|---|---|---|
| customer_id | STRING | Unique customer identifier | Yes |
| customer_name | STRING | Customer name | Yes |
| email | STRING | Customer email | Yes |
| phone | STRING | Customer phone number | No |
| city | STRING | Customer city | Yes |
| created_at | TIMESTAMP | Customer creation timestamp | Yes |

---

# 3. Order

| Column | Data Type | Description | Required |
|---|---|---|---|
| order_id | STRING | Unique order identifier | Yes |
| customer_id | STRING | Customer associated with order | Yes |
| warehouse_id | STRING | Warehouse processing the order | Yes |
| order_date | TIMESTAMP | Order creation timestamp | Yes |
| order_amount | DECIMAL | Order value | Yes |
| order_status | STRING | Current order status | Yes |

---

# 4. Delivery

| Column | Data Type | Description | Required |
|---|---|---|---|
| delivery_id | STRING | Unique delivery identifier | Yes |
| order_id | STRING | Associated order | Yes |
| driver_id | STRING | Assigned driver | Yes |
| vehicle_id | STRING | Assigned vehicle | Yes |
| warehouse_id | STRING | Origin warehouse | Yes |
| pickup_time | TIMESTAMP | Package pickup time | Yes |
| promised_delivery_time | TIMESTAMP | Expected delivery time | Yes |
| delivery_time | TIMESTAMP | Actual delivery time | No |
| delivery_status | STRING | Delivery status | Yes |

---

# 5. Driver

| Column | Data Type | Description | Required |
|---|---|---|---|
| driver_id | STRING | Unique driver identifier | Yes |
| driver_name | STRING | Driver name | Yes |
| phone | STRING | Driver phone | No |
| warehouse_id | STRING | Assigned warehouse | Yes |
| joining_date | DATE | Driver joining date | Yes |
| status | STRING | Driver current status | Yes |

---

# 6. Vehicle

| Column | Data Type | Description | Required |
|---|---|---|---|
| vehicle_id | STRING | Unique vehicle identifier | Yes |
| vehicle_type | STRING | Vehicle category | Yes |
| registration_number | STRING | Vehicle registration | Yes |
| warehouse_id | STRING | Assigned warehouse | Yes |
| fuel_type | STRING | Fuel type | Yes |
| status | STRING | Vehicle status | Yes |

---

# 7. Warehouse

| Column | Data Type | Description | Required |
|---|---|---|---|
| warehouse_id | STRING | Unique warehouse identifier | Yes |
| warehouse_name | STRING | Warehouse name | Yes |
| city | STRING | Warehouse city | Yes |
| state | STRING | Warehouse state | Yes |
| capacity | INTEGER | Package capacity | Yes |
| status | STRING | Warehouse status | Yes |

---

# 8. Vehicle Event

| Column | Data Type | Description | Required |
|---|---|---|---|
| event_id | STRING | Unique event identifier | Yes |
| vehicle_id | STRING | Vehicle identifier | Yes |
| timestamp | TIMESTAMP | Event timestamp | Yes |
| latitude | DOUBLE | GPS latitude | Yes |
| longitude | DOUBLE | GPS longitude | Yes |
| speed | DOUBLE | Vehicle speed | Yes |
| fuel_level | DOUBLE | Remaining fuel percentage | Yes |

---

# 9. Data Layer Meaning

## Landing

Original data received from source systems.

## Bronze

Raw historical copy of source data with ingestion metadata.

## Silver

Cleaned, validated, standardized data.

## Gold

Business-ready analytical datasets.

## Quarantine

Invalid or rejected records.

## Archive

Historical data retained for long-term storage.