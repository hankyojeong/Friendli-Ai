import sqlite3
import pandas as pd
FILE = "C:/Users/hanky/OneDrive/Desktop/서울대학교/IDEA 연구실/LLM/Friendli AI/data/1_국내체류외국인.xlsx"
TBL_RAW = "1_tb_resident_foreigners"
Q_TBL = '"' + TBL_RAW + '"'

# load
if FILE.lower().endswith(".xlsx"): 
    df = pd.read_excel(FILE)
else:
    df = pd.read_csv(FILE, encoding="utf-8-sig", low_memory=False)

con = sqlite3.connect(":memory:")
df.to_sql(TBL_RAW, con, index=False)

# SQL: 2023~2025년 1월 장기체류(장기체류거소+장기체류등록) 월별 합계 + 전년 대비 증감률
sql = '''
WITH annual_data AS (
  SELECT 
    "p_year",
    COALESCE(SUM(CAST("cnt" AS INT)), 0) AS total
  FROM {Q_TBL}
  WHERE "p_month" = 1
    AND "p_year" IN (2023, 2024, 2025)
    AND UPPER(TRIM("category")) IN ('장기체류거소', '장기체류등록')
  GROUP BY "p_year"
  ORDER BY "p_year"
)
SELECT 
  "p_year",
  "total",
  ROUND(100.0 * ("total" - LAG("total", 1) OVER()) / NULLIF(LAG("total", 1) OVER(), 0), 2) AS growth_rate_pct
FROM annual_data
ORDER BY "p_year"
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))