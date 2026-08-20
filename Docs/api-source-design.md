# REST API Source Design

## 1. Purpose

The REST API represents an external delivery-partner system used by FastTrack Logistics.

The API provides delivery, driver, and vehicle information that will be integrated into the central data platform.

The API will be simulated locally so that the project is completely reproducible and we can intentionally test API failures.

---

# 2. API Resources

The API will initially expose:

- Deliveries
- Drivers
- Vehicles
- Health Check

---

# 3. API Endpoints

```text
GET /api/v1/deliveries
GET /api/v1/drivers
GET /api/v1/vehicles
GET /api/v1/health