import pymysql

host = '10.120.26.3'
port = 25000
user = 'root'
passwd = 'example'
db = 'mysql'
charset = 'utf8mb4'

a = 'tt2395469'
b = 'tt1528100'
c = 'tt0269095'

conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
cursor = conn.cursor()
sql_set = 'SET SESSION sql_mode=(SELECT REPLACE(@@sql_mode, "ONLY_FULL_GROUP_BY,", ""));'

sql = 'SELECT COUNT(out_id)AS times, sum(sim)/COUNT(out_id) AS avg_sim, sum(con) AS sum_con, out_id, movie_name\n'\
+'FROM movie_spark\n'\
+'WHERE in_id="%s" OR in_id="%s" OR in_id="%s"\n' % (a, b, c)\
+'GROUP BY out_id\n'\
+'HAVING avg(sim)\n'\
+'ORDER BY times DESC , sum_con DESC\n'\
+'LIMIT 10;\n'

ce_set = cursor.execute(sql_set)
ce = cursor.execute(sql)
content = cursor.fetchall()

print(content)
[print(i[4]) for i in content]

cursor.close()
conn.close()
