# 📊 ETL Workshop 1 — Data Engineer Challenge

This repository contains the full solution to **Workshop 1** of the ETL course, designed as a **technical challenge for Data Engineers**.

It implements an **ETL** pipeline (Extract → Transform → Load) that ingests a CSV of candidate applications, loads the raw data into a **SQLite** data warehouse, transforms it into a **star schema**, and generates **KPIs** and **visualizations** directly from the warehouse.

---

## 🧠 ETL

| ⚙️ Step        | 🔍 Description |
|---------------|----------------|
| 📥 **Extract** | Read raw data from CSV file |
| 🐬 **Load**    | Store unmodified data in staging table in SQLite |
| 🐍 **Transform** | Run all transformations and business logic using SQL inside the DW |
| 📊 **KPIs**    | Query dimensional model to compute metrics |
| 📈 **Visuals** | Generate Ruby Red charts using Python & Matplotlib |

---

## 📁 Project Structure

```
etl_workshop/
├── data/
│   └── candidates.csv              # Raw CSV file
├── docs/
│   └── schema_star.png             # Star Schema diagram
├── sql/
│   └── queries.sql                 # KPI queries in SQL
├── src/
│   ├── etl.py                      # ELT pipeline using SQL
│   └── visuals.py                  # Chart generation (Ruby Red theme)
├── visuals/                        # Auto-generated .png charts
├── dw_hiring.db                    # SQLite DW (generated)
├── requirements.txt
└── .gitignore
```

---

## 🐍 Requirements

- Python **3.8+**
- Required packages:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

### 1. Run ETL pipeline

```bash
python src/etl.py
```

This will:
- Load raw data into `stg_candidates_raw`
- Build dimensions: `DimDate`, `DimCountry`, `DimSeniority`, `DimTechnology`
- Create fact table: `FactHiring`

### 2. Generate visualizations

```bash
python src/visuals.py
```

Generates `.png` charts in `visuals/`

---

## 🗂️ Star Schema

- **FactHiring**
  - `date_id`, `country_id`, `seniority_id`, `technology_id`
  - `hired`, `code_score`, `tech_score`
- **DimDate**
- **DimCountry**
- **DimSeniority**
- **DimTechnology**
## Architecture
<img width="1001" height="730" alt="image" src="https://github.com/user-attachments/assets/1a812e14-9eda-4bb6-9d1e-1bc83d9d44e9" />

📌 See: `docs/schema_star.png`
⭐ Star Schema Justification

The star schema is the core of this Data Warehouse design. It consists of:

FactHiring (Fact Table):

This table contains the key metrics for analysis, such as hired, code_score, and tech_score, representing the outcomes of the hiring process.

It connects to the dimensions via foreign keys: date_id, country_id, seniority_id, and technology_id.

DimDate (Dimension Table):

Stores date-related attributes (year, month, day) linked to each hiring record through date_id.

Allows for temporal analysis, enabling KPIs like "Hires by Year."

DimCountry (Dimension Table):

Stores the country for each candidate, linked to the FactHiring table through country_id.

Helps in analyzing hires based on geographic locations (e.g., "Hires by Country").

DimSeniority (Dimension Table):

Contains information about the candidate’s seniority level (e.g., Intern, Junior, Senior), linked to FactHiring through seniority_id.

Provides insights into the distribution of hires by experience level.

DimTechnology (Dimension Table):

Includes the technologies (e.g., Python, Java, etc.) associated with each hire, connected to FactHiring via technology_id.

Facilitates analysis of hires by technology, enabling KPIs like "Hires by Technology."

Why Star Schema?

The Star Schema simplifies query writing and improves performance, as it provides clear separation between facts and dimensions.

This schema allows easy, scalable analysis of hiring metrics based on multiple dimensions (e.g., by country, by technology, by seniority level).

The Fact Table stores detailed numeric data, while the Dimension Tables store descriptive attributes, making it easier to aggregate and filter data.
---

## 🧮 KPIs Available

- Hires by Technology (Top 12)
- Hires by Year
- Hires by Seniority
- Hires by Country (Grouped by Year)
- Hires by Seniority and Technology
- Hire Percentage by Seniority (%)
- 
All queries are available in `sql/queries.sql`.

---

## 📈 Example Visualizations

Charts are saved in `/visuals`:

| 📊 Chart Description                      | 📄 Filename                            |
|------------------------------------------|----------------------------------------|
| Hires by Technology (Top 12)             | `kpi_tech_top12.png`                   |
| Hires by Year (Line Chart)               | `kpi_year.png`                         |
| Hires by Seniority                       | `kpi_seniority.png`                    |
| Hires by Country × Year (Grouped Bars)   | `kpi_country_year_grouped.png`         |
| Hires by Seniority and Top 3 Technologies| `kpi_hires_by_seniority_and_tech.png`  |
| Hire Percentage by Seniority (%)         | `kpi_hires_pct_seniority.png`          |



All generated using `matplotlib` with a unified Ruby Red theme (`#9B111E`).

---

## 🧪 Testing SQL Queries

You can run the queries manually in:

- DB Browser for SQLite
- SQLite CLI
- Python:

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///dw_hiring.db")
df = pd.read_sql("SELECT * FROM FactHiring LIMIT 5;", engine)
print(df)
```

---

## 🐬 SQL Logic: Transformations inside the DW

All data transformations happen in SQL, inside SQLite, after loading the raw CSV into `stg_candidates_raw`.

### Examples:

```sql
-- HIRED logic
CASE
  WHEN CAST("Code Challenge Score" AS INT) >= 7
   AND CAST("Technical Interview Score" AS INT) >= 7 THEN 1
  ELSE 0
END

-- Extracting dates
STRFTIME('%Y', "Application Date") AS year
```

---

# 1) Clonar el repositorio
git clone https://github.com/EstebanC111s/ETL_Workshop1.git

# 2) Entrar a la carpeta del proyecto
```bash
cd ETL_Workshop1
```

# 3) Abrir en Visual Studio Code
```bash
code .
```

# 4) (Opcional) Crear entorno y deps
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

# 5) Ejecutar el pipeline y las gráficas
```bash
python src/etl.py
python src/visuals.py
```




Made with 🐬 SQL + 🐍 Python — for the ETL Workshop.
