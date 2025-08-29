from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

def main():
    root = Path(__file__).resolve().parents[1]
    csv_path = root / "data" / "candidates.csv"
    db_path  = root / "dw_hiring.db"

    # 1) EXTRACT + LOAD (staging crudo)
    df = pd.read_csv(csv_path, delimiter=";")  # sin limpiar
    eng = create_engine(f"sqlite:///{db_path}", echo=False)

    with eng.begin() as conn:
        # Staging
        conn.exec_driver_sql("DROP TABLE IF EXISTS stg_candidates_raw")
        df.to_sql("stg_candidates_raw", conn, if_exists="replace", index=False)

        # 2) TRANSFORM en SQL (sentencias separadas)

        # --- DimCountry ---
        conn.exec_driver_sql("DROP TABLE IF EXISTS DimCountry")
        conn.exec_driver_sql("""
            CREATE TABLE DimCountry (
                country_id INTEGER PRIMARY KEY AUTOINCREMENT,
                country    TEXT UNIQUE
            )
        """)
        conn.exec_driver_sql("""
            INSERT INTO DimCountry(country)
            SELECT DISTINCT Country
            FROM stg_candidates_raw
            WHERE Country IS NOT NULL AND TRIM(Country) <> ''
        """)

        # --- DimSeniority ---
        conn.exec_driver_sql("DROP TABLE IF EXISTS DimSeniority")
        conn.exec_driver_sql("""
            CREATE TABLE DimSeniority (
                seniority_id INTEGER PRIMARY KEY AUTOINCREMENT,
                seniority    TEXT UNIQUE
            )
        """)
        conn.exec_driver_sql("""
            INSERT INTO DimSeniority(seniority)
            SELECT DISTINCT Seniority
            FROM stg_candidates_raw
            WHERE Seniority IS NOT NULL AND TRIM(Seniority) <> ''
        """)

        # --- DimTechnology ---
        conn.exec_driver_sql("DROP TABLE IF EXISTS DimTechnology")
        conn.exec_driver_sql("""
            CREATE TABLE DimTechnology (
                technology_id INTEGER PRIMARY KEY AUTOINCREMENT,
                technology    TEXT UNIQUE
            )
        """)
        conn.exec_driver_sql("""
            INSERT INTO DimTechnology(technology)
            SELECT DISTINCT Technology
            FROM stg_candidates_raw
            WHERE Technology IS NOT NULL AND TRIM(Technology) <> ''
        """)

        # --- DimDate ---
        conn.exec_driver_sql("DROP TABLE IF EXISTS DimDate")
        conn.exec_driver_sql("""
            CREATE TABLE DimDate (
                date_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                full_date TEXT UNIQUE,
                year      INTEGER,
                month     INTEGER,
                day       INTEGER
            )
        """)
        conn.exec_driver_sql("""
            INSERT INTO DimDate(full_date, year, month, day)
            SELECT DISTINCT
                   DATE([Application Date])                           AS full_date,
                   CAST(STRFTIME('%Y', DATE([Application Date])) AS INT) AS year,
                   CAST(STRFTIME('%m', DATE([Application Date])) AS INT) AS month,
                   CAST(STRFTIME('%d', DATE([Application Date])) AS INT) AS day
            FROM stg_candidates_raw
            WHERE [Application Date] IS NOT NULL AND TRIM([Application Date]) <> ''
        """)

        # --- FactHiring ---
        conn.exec_driver_sql("DROP TABLE IF EXISTS FactHiring")
        conn.exec_driver_sql("""
            CREATE TABLE FactHiring (
                fact_id       INTEGER PRIMARY KEY AUTOINCREMENT,
                date_id       INTEGER,
                country_id    INTEGER,
                seniority_id  INTEGER,
                technology_id INTEGER,
                hired         INTEGER,
                code_score    INTEGER,
                tech_score    INTEGER,
                FOREIGN KEY(date_id)       REFERENCES DimDate(date_id),
                FOREIGN KEY(country_id)    REFERENCES DimCountry(country_id),
                FOREIGN KEY(seniority_id)  REFERENCES DimSeniority(seniority_id),
                FOREIGN KEY(technology_id) REFERENCES DimTechnology(technology_id)
            )
        """)
        conn.exec_driver_sql("""
            INSERT INTO FactHiring (date_id, country_id, seniority_id, technology_id, hired, code_score, tech_score)
            SELECT
                d.date_id,
                c.country_id,
                s.seniority_id,
                t.technology_id,
                CASE
                    WHEN CAST([Code Challenge Score] AS INT) >= 7
                     AND CAST([Technical Interview Score] AS INT) >= 7 THEN 1
                    ELSE 0
                END AS hired,
                CAST([Code Challenge Score] AS INT)      AS code_score,
                CAST([Technical Interview Score] AS INT) AS tech_score
            FROM stg_candidates_raw r
            JOIN DimDate       d ON d.full_date   = DATE(r.[Application Date])
            JOIN DimCountry    c ON c.country     = r.Country
            JOIN DimSeniority  s ON s.seniority   = r.Seniority
            JOIN DimTechnology t ON t.technology  = r.Technology
        """)

    # Resumen
    with eng.connect() as c:
        dim_date_n = c.execute(text("SELECT COUNT(*) FROM DimDate")).scalar_one()
        dim_ctry_n = c.execute(text("SELECT COUNT(*) FROM DimCountry")).scalar_one()
        dim_sen_n  = c.execute(text("SELECT COUNT(*) FROM DimSeniority")).scalar_one()
        dim_tech_n = c.execute(text("SELECT COUNT(*) FROM DimTechnology")).scalar_one()
        fact_n     = c.execute(text("SELECT COUNT(*) FROM FactHiring")).scalar_one()

    print(f"DW listo en {db_path}")
    print(f"DimDate:{dim_date_n}  DimCountry:{dim_ctry_n}  DimSeniority:{dim_sen_n}  DimTechnology:{dim_tech_n}")
    print(f"FactHiring:{fact_n}")

if __name__ == "__main__":
    main()
