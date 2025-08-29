# src/visuals.py
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Setup
ROOT = Path(__file__).resolve().parents[1]
DB   = ROOT / "dw_hiring.db"
OUT  = ROOT / "visuals"
OUT.mkdir(exist_ok=True)

engine = create_engine(f"sqlite:///{DB}", echo=False)
RUBY_RED = "#9B111E"

def save_bar(df, x, y, title, fname, rotate=False):
    plt.figure()
    plt.bar(df[x].astype(str), df[y].astype(float), color=RUBY_RED)
    if rotate:
        plt.xticks(rotation=45, ha="right")
    plt.title(title)
    plt.xlabel(x); plt.ylabel(y)
    plt.tight_layout()
    plt.savefig(OUT / fname, dpi=140)
    plt.close()

def save_line(df, x, y, title, fname):
    plt.figure()
    plt.plot(df[x].astype(str), df[y].astype(float), marker="o", color=RUBY_RED)
    plt.title(title)
    plt.xlabel(x); plt.ylabel(y)
    plt.tight_layout()
    plt.savefig(OUT / fname, dpi=140)
    plt.close()

# 1) Hires by Technology (Top 12)
kpi_tech = pd.read_sql("""
SELECT t.technology, SUM(f.hired) AS hires
FROM FactHiring f
JOIN DimTechnology t ON f.technology_id = t.technology_id
GROUP BY t.technology
ORDER BY hires DESC
LIMIT 12;
""", engine)
save_bar(kpi_tech, "technology", "hires",
         "Hires by Technology (Top 12)", "kpi_tech_top12.png", rotate=True)

# 2) Hires by Year
kpi_year = pd.read_sql("""
SELECT d.year, SUM(f.hired) AS hires
FROM FactHiring f
JOIN DimDate d ON f.date_id = d.date_id
GROUP BY d.year
ORDER BY d.year;
""", engine)
save_line(kpi_year, "year", "hires", "Hires by Year", "kpi_year.png")

# 3) Hires by Seniority
kpi_sen = pd.read_sql("""
SELECT s.seniority, SUM(f.hired) AS hires
FROM FactHiring f
JOIN DimSeniority s ON f.seniority_id = s.seniority_id
GROUP BY s.seniority
ORDER BY hires DESC;
""", engine)
save_bar(kpi_sen, "seniority", "hires",
         "Hires by Seniority", "kpi_seniority.png", rotate=True)

# 4) Hires by Country (USA, Brazil, Colombia, Ecuador) per Year
kpi_country_year = pd.read_sql("""
SELECT c.country, d.year, SUM(f.hired) AS hires
FROM FactHiring f
JOIN DimCountry c ON f.country_id = c.country_id
JOIN DimDate d ON f.date_id = d.date_id
WHERE c.country IN ('United States','Brazil','Colombia','Ecuador')
GROUP BY c.country, d.year
ORDER BY d.year, c.country;
""", engine)

pivot = kpi_country_year.pivot(index="year", columns="country", values="hires").fillna(0)

colors = ['#9B111E', '#B22222', '#D62728', '#E34234']  # ruby red shades or any other

plt.figure()
bar_width = 0.2
x_labels = pivot.index.astype(str).tolist()
x_positions = list(range(len(x_labels)))
countries = list(pivot.columns)

for i, country in enumerate(countries):
    offsets = [pos + (i - (len(countries)-1)/2) * bar_width for pos in x_positions]
    heights = pivot[country].astype(float).to_numpy()
    plt.bar(offsets, heights, width=bar_width, label=country, color=colors[i % len(colors)])

plt.xticks(x_positions, x_labels)
plt.title("Hires by Year (Grouped by Country)")
plt.xlabel("Year")
plt.ylabel("Hires")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "kpi_country_year_grouped.png", dpi=140)
plt.close()

# 5) Extra KPI: Global Hire Rate (%)
hire_rate = pd.read_sql("SELECT ROUND(AVG(hired)*100,2) AS hire_rate_pct FROM FactHiring;", engine)
plt.figure()
plt.bar(["Hire Rate %"], hire_rate["hire_rate_pct"].astype(float), color=RUBY_RED)
plt.title("Global Hire Rate (%)")
plt.tight_layout()
plt.savefig(OUT / "kpi_hire_rate.png", dpi=140)
plt.close()

# 6) Extra KPI: Average Scores by Technology (Top 10 by code score)
avg_scores = pd.read_sql("""
SELECT t.technology,
       ROUND(AVG(f.code_score), 2) AS avg_code_score,
       ROUND(AVG(f.tech_score), 2) AS avg_tech_score
FROM FactHiring f
JOIN DimTechnology t ON f.technology_id = t.technology_id
GROUP BY t.technology
ORDER BY avg_code_score DESC
LIMIT 10;
""", engine)

save_bar(avg_scores, "technology", "avg_code_score",
         "Avg. Code Score by Technology (Top 10)", "kpi_avg_code_score_top10.png", rotate=True)
save_bar(avg_scores.sort_values("avg_tech_score", ascending=False), "technology", "avg_tech_score",
         "Avg. Tech Score by Technology (Top 10)", "kpi_avg_tech_score_top10.png", rotate=True)

print(f"✅ Charts successfully saved to: {OUT}")
