import sqlite3
import pandas as pd
FILE = "C:/Users/hanky/OneDrive/Desktop/서울대학교/IDEA 연구실/LLM/Friendli AI/data/2_장기체류외국인_지역별_현황.csv"
TBL_RAW = "2_tb_long_term_foreigners_by_region"
Q_TBL = '"{}"'.format(TBL_RAW)

# load
if FILE.lower().endswith(".xlsx"): 
    df = pd.read_excel(FILE)
else:
    df = pd.read_csv(FILE, encoding="utf-8-sig", low_memory=False)

con = sqlite3.connect(":memory:")
df.to_sql(TBL_RAW, con, index=False)

# SQL: 2025-04 / 경기 화성시 / 연령대 분포 (table_nm=4)
sql = '''
SELECT 
  UPPER(TRIM("age")) AS age_group,
  COALESCE(SUM(CAST("cnt" AS INT)), 0) AS total_count
FROM {Q_TBL}
WHERE 
  -- base_ym = 2025-04 (normalize and match)
  REPLACE(REPLACE(REPLACE(TRIM("base_ym"),'-',''),'_',''),'.','') = '202504'
  AND UPPER(TRIM("table_nm")) = '4'  -- 연령대 데이터
  AND (
    UPPER(TRIM("sido")) IN ('경기','경기도') OR 
    UPPER(TRIM("sido")) LIKE '경기%'
  )
  AND (
    UPPER(TRIM("sigungu")) IN ('화성','화성시') OR 
    UPPER(TRIM("sigungu")) LIKE '화성%'
  )
GROUP BY UPPER(TRIM("age"))
ORDER BY age_group
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))