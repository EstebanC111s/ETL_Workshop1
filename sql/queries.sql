-- KPI 1: Hires por tecnología
SELECT t.technology, SUM(f.hired) AS hires
FROM FactHiring f
JOIN DimTechnology t ON f.technology_id = t.technology_id
GROUP BY t.technology
ORDER BY hires DESC;

-- KPI 2: Hires por año
SELECT d.year, SUM(f.hired) AS hires
FROM FactHiring f
JOIN DimDate d ON f.date_id = d.date_id
GROUP BY d.year
ORDER BY d.year;

-- KPI 3: Hires por seniority
SELECT s.seniority, SUM(f.hired) AS hires
FROM FactHiring f
JOIN DimSeniority s ON f.seniority_id = s.seniority_id
GROUP BY s.seniority
ORDER BY hires DESC;

-- KPI 4: Hires por país (USA, Brasil, Colombia, Ecuador) por año
SELECT c.country, d.year, SUM(f.hired) AS hires
FROM FactHiring f
JOIN DimCountry c ON f.country_id = c.country_id
JOIN DimDate d ON f.date_id = d.date_id
WHERE c.country IN ('United States', 'Brazil', 'Colombia', 'Ecuador')
GROUP BY c.country, d.year
ORDER BY c.country, d.year;

-- KPI 5 (extra): En qué tecnologías están contratando gente con menos experiencia
SELECT Technology,
       ROUND(AVG(YOE), 2) AS avg_yoe_hired
FROM stg_candidates_raw
WHERE CAST("Code Challenge Score" AS INT) >= 7
  AND CAST("Technical Interview Score" AS INT) >= 7
GROUP BY Technology;


-- KPI 6 (extra): Países tienen más contrataciones de perfiles avanzados
SELECT c.country,
       ROUND(
         100.0 * SUM(CASE WHEN s.seniority IN ('Lead', 'Mid-Level') AND f.hired = 1 THEN 1 ELSE 0 END) /
         NULLIF(SUM(f.hired), 0), 2
       ) AS pct_senior_hires
FROM FactHiring f
JOIN DimCountry c ON f.country_id = c.country_id
JOIN DimSeniority s ON f.seniority_id = s.seniority_id
GROUP BY c.country
HAVING SUM(f.hired) >= 10;


