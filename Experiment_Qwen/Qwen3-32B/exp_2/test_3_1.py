import sqlite3
import pandas as pd
FILE = "C:/Users/hanky/OneDrive/Desktop/서울대학교/IDEA 연구실/LLM/Friendli AI/data/3_외국인근로자.xlsx"
TBL_RAW = "3_tb_foreign_workers_permit"
Q_TBL = '"' + TBL_RAW + '"'

if FILE.lower().endswith(".xlsx"):
    df = pd.read_excel(FILE)
else:
    df = pd.read_csv(FILE, encoding="utf-8-sig", low_memory=False)

con = sqlite3.connect(":memory:")
df.to_sql(TBL_RAW, con, index=False)

sql = '''
SELECT
  REPLACE(REPLACE(REPLACE(TRIM("base_ym"),'-',''),'_',''),'.','') AS base_ym,
  COALESCE(SUM(CAST(upjong AS INT)), 0) AS total_workers
FROM {Q_TBL}
GROUP BY REPLACE(REPLACE(REPLACE(TRIM("base_ym"),'-',''),'_',''),'.','')
ORDER BY CAST(REPLACE(REPLACE(REPLACE(TRIM("base_ym"),'-',''),'_',''),'.','') AS INT)
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))