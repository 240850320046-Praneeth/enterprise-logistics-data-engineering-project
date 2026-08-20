
---

# 5. `architecture.md`

Don't make this complicated yet.

Paste:

```markdown
# System Architecture

## 1. Architecture Objective

The platform will provide an end-to-end data pipeline for batch and real-time logistics data.

The architecture will support:

- Batch ingestion
- Streaming ingestion
- Cloud data lake storage
- Data transformation
- Data quality
- Incremental processing
- Analytical modeling
- Business intelligence
- Monitoring

---

# 2. High-Level Architecture

```text
                    SOURCE SYSTEMS
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
   SQL Server        REST API        CSV / JSON
        |                |                |
        +----------------+----------------+
                         |
                         v
                Azure Data Factory
                         |
                         v
                     ADLS Gen2
                         |
                      Landing
                         |
                         v
                      Bronze
                         |
                         v
                 Azure Databricks
                     PySpark
                         |
                         v
                      Silver
                         |
                         v
                       Gold
                         |
                 +-------+-------+
                 |               |
                 v               v
              Synapse         Power BI
                 |               |
                 +-------+-------+
                         |
                         v
                  Business Users