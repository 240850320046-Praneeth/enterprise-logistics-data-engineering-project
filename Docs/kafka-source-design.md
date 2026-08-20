```markdown
# Kafka Source Design

## 1. Purpose

Kafka will simulate the real-time Vehicle Tracking System of FastTrack Logistics.

Vehicles continuously generate GPS and operational events while they are active.

Unlike SQL, API, and warehouse files, vehicle telemetry is real-time data and should not wait for an hourly batch process.

---

# 2. Source System

Source:

Vehicle Tracking System

Technology:

Apache Kafka

Processing Type:

Streaming

Data Format:

JSON

Expected Frequency:

Real-time

---

# 3. Kafka Topic

Topic:

```text
vehicle-events


