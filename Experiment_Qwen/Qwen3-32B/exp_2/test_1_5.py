import sqlite3
import pandas as pd
FILE = "C:/Users/hanky/OneDrive/Desktop/서울대학교/IDEA 연구실/LLM/Friendli AI/data/1_국내체류외국인.xlsx"
TBL_RAW = "1_tb_resident_foreigners"
Q_TBL = '"' + TBL_RAW + '"'

if FILE.lower().endswith(".xlsx"): 
    df = pd.read_excel(FILE)
else: 
    df = pd.read_csv(FILE, encoding="utf-8-sig", low_memory=False)

con = sqlite3.connect(":memory:")
df.to_sql(TBL_RAW, con, index=False)

sql = '''
WITH LongTerm AS (
  SELECT 
    "p_year",
    COALESCE(SUM(CAST("cnt" AS INT)), 0) AS total_cnt
  FROM {Q_TBL}
  WHERE 
    UPPER(TRIM("category")) IN ('장기체류거소', '장기체류등록') AND 
    "p_month" = 3 AND 
    "p_year" BETWEEN 2023 AND 2025
  GROUP BY "p_year"
)
SELECT 
  "p_year",
  "total_cnt",
  ROUND(
    100.0 * (total_cnt - LAG(total_cnt, 1, 0) OVER (ORDER BY "p_year")), 
    1
  ) / NULLIF(LAG(total_cnt, 1) OVER (ORDER BY "p_year"), 0) AS yoy_change_pct
FROM LongTerm
ORDER BY "p_year"
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))