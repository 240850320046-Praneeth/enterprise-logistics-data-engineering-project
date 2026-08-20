# Business Rules

## 1. Purpose

This document defines the business rules that will be implemented in the data processing and data quality layers.

---

# 2. Order Rules

### Rule 1
Every order must have a unique order_id.

### Rule 2
Every order must reference an existing customer.

### Rule 3
Every order must reference an existing warehouse.

### Rule 4
Order amount cannot be negative.

### Rule 5
Order status must belong to the approved status list.

Approved statuses:

```text
CREATED
PROCESSING
DISPATCHED
DELIVERED
CANCELLED