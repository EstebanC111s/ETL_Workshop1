# ETL Workshop 1 - Data Engineer Challenge

Este proyecto corresponde al **Workshop 1 del curso ETL**.  
Simula un reto técnico de entrevista para un perfil **Data Engineer**, en el que se construye un proceso **ETL (Extract, Transform, Load)** completo a partir de un dataset con 50,000 candidatos de procesos de selección.

---

## 📌 Objetivo

1. **Extract** → Cargar datos desde un CSV con información de candidatos.  
2. **Transform** → Aplicar reglas de negocio (ejemplo: un candidato es HIRED si sus dos puntajes ≥ 7) y organizar los datos en un modelo dimensional (Star Schema).  
3. **Load** → Cargar la información en un **Data Warehouse** (SQLite en este caso).  
4. **KPIs y Visualizaciones** → Consultar el DW para obtener métricas y gráficas que permitan analizar contrataciones por país, tecnología, seniority, etc.

---

## 🗂️ Estructura del proyecto

etl_workshop/
│── etl.py # Proceso ETL completo (Extract, Transform, Load)
│── queries.sql # Consultas SQL para KPIs
│── dw_hiring.db # Data Warehouse en SQLite (se genera al correr etl.py)
│── schema_star.png # Diagrama del Star Schema
│── README.md # Documentación del proyecto
│── requirements.txt # Librerías necesarias
│── .gitignore # Archivos a ignorar en GitHub
