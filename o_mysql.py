import pymysql

host = '10.120.26.3'
port = 3307
user = 'root'
passwd = 'example'
db = 'mysql'
charset = 'utf8mb4'

conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
table_name='ace_table'
sql_create_table='CREATE TABLE IF NOT EXISTS {}(' \
                     'rank TEXT,movie_name TEXT,worldwide_gross TEXT,' \
                     'domestic_gross TEXT,domestic_gross_percent TEXT,' \
                     'foreign_gross TEXT,foreign_gross_percent TEXT);'.format(table_name)
cursor = conn.cursor()
cursor.execute(sql_create_table)

sql_insert = 'INSERT INTO {} (rank,movie_name,worldwide_gross,domestic_gross,domestic_gross_percent,foreign_gross,foreign_gross_percent) ' \
              'VALUES ("fu","bad","suck","shit","hello","hi","bro");'.format(table_name)

ce=cursor.execute(sql_insert)
conn.commit()

cursor.close()
conn.close()
