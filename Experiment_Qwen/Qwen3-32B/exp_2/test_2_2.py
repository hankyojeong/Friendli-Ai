import sqlite3
import pandas as pd
FILE = "C:/Users/hanky/OneDrive/Desktop/서울대학교/IDEA 연구실/LLM/Friendli AI/data/2_장기체류외국인_지역별_현황.csv"
TBL_RAW = "2_tb_long_term_foreigners_by_region"
Q_TBL = '"' + TBL_RAW + '"'

if FILE.lower().endswith(".xlsx"): 
    df = pd.read_excel(FILE)
else: 
    df = pd.read_csv(FILE, encoding="utf-8-sig", low_memory=False)

con = sqlite3.connect(":memory:")
df.to_sql(TBL_RAW, con, index=False)

sql = '''
SELECT 
  "age" AS age_group,
  COALESCE(SUM(CAST("cnt" AS INT)), 0) AS total_count
FROM {Q_TBL}
WHERE 
  UPPER(TRIM("base_ym")) = '202406' AND
  (UPPER(TRIM("sido")) IN ('경기','경기도') OR UPPER(TRIM("sido")) LIKE '경기%') AND
  (UPPER(TRIM("sigungu")) IN ('화성','화성시') OR UPPER(TRIM("sigungu")) LIKE '화성%') AND
  UPPER(TRIM("gbn")) = '거소외국인' AND
  "table_nm" = '4'
GROUP BY "age"
ORDER BY 
  CASE "age"
    WHEN '0~9' THEN 1
    WHEN '10~19' THEN 2
    WHEN '20~29' THEN 3
    WHEN '30~39' THEN 4
    WHEN '40~49' THEN 5
    WHEN '50~59' THEN 6
    WHEN '60~69' THEN 7
    WHEN '70~79' THEN 8
    WHEN '80~' THEN 9
    ELSE 10
  END
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))