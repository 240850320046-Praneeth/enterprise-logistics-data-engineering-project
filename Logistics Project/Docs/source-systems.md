# Source Systems

## 1. Overview

FastTrack Logistics receives data from multiple source systems.

Each source has a different data format, ingestion method, and processing requirement.

The platform will support both batch and streaming sources.

---

# 2. Source System Summary

| Source System | Data | Format | Processing Type | Frequency |
|---|---|---|---|---|
| Order Management System | Customers, Orders | SQL | Batch | Hourly |
| Delivery Partner API | Delivery information | JSON | Batch/API | Hourly |
| Warehouse System | Package and dispatch data | CSV/JSON | Batch | Daily/Hourly |
| Vehicle Tracking System | GPS and vehicle events | JSON/Kafka | Streaming | Real-time |
| Application Logs | Application events | JSON | Streaming/Batch | Near real-time |

---

# 3. Order Management System

## Technology

SQL Server

## Processing Type

Batch

## Frequency

Hourly

## Main Entities

- Customers
- Orders
- Deliveries
- Drivers
- Vehicles
- Warehouses

## Purpose

The Order Management System contains operational order information.

It represents the beginning of the logistics process.

## Example Data

```text
order_id
customer_id
warehouse_id
order_date
order_amount
order_status