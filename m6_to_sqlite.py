import sqlite3

j = 0
conn=sqlite3.connect("data_set.sqlite")
sql_create_table='CREATE TABLE IF NOT EXISTS aka(' \
    'titleId TEXT,ordering TEXT,title TEXT,' \
    'region TEXT,language TEXT,types TEXT, ' \
    'attributes TEXT,isOriginalTitle TEXT);'

cursor = conn.cursor()
cursor.execute(sql_create_table)
with open('./old/set/aka.tsv', 'r', encoding='utf-8') as e:
    while True:
        lis = e.readline()
        lis2 = lis.split('\t')
        # print(lis2)
        if not lis:
            break

        sql_insert = 'INSERT INTO aka (titleId,ordering,title,region,language,types,attributes,isOriginalTitle) ' \
              'VALUES ("{}","{}","{}","{}","{}","{}","{}","{}");'\
            .format(str(lis2[0]).replace('"','＂'),
                    str(lis2[1]).replace('"','＂'),
                    str(lis2[2]).replace('"', '＂'),
                    str(lis2[3]).replace('"', '＂'),
                    str(lis2[4]).replace('"', '＂'),
                    str(lis2[5]).replace('"', '＂'),
                    str(lis2[6]).replace('"', '＂'),
                    str(lis2[7]).replace('"','＂'))
        ce=cursor.execute(sql_insert)
        conn.commit()
        j += 1
        print('EI：', ce,'No：', j)

cursor.close()
conn.close()

import sqlite3

j = 0
conn=sqlite3.connect("rating_200w_n.sqlite")
sql_create_table='CREATE TABLE IF NOT EXISTS w200_n(' \
    'date1 VARCHAR(12), day2 INT(5),user TEXT, name1 VARCHAR(12),ranting INT(2), usernum INT(7),movienum INT(4));'

cursor = conn.cursor()
cursor.execute(sql_create_table)

with open('./usernum99.tsv', 'r', encoding='ISO-8859-1') as e:
    lis = e.readlines()
for i in lis:
    i = i.split('\t')
    sql_insert = 'INSERT INTO w200_n (date1, day2 ,user, name1 ,ranting,usernum,movienum) VALUES ("{}","{}","{}","{}","{}","{}","{}");'\
        .format(str(i[0]).replace('"','＂'),
                str(i[1]).replace('"', '＂'),
                str(i[2]).replace('"', '＂'),
                str(i[3]).replace('"', '＂'),
                str(i[4]).replace('"', '＂'),
                str(i[5]).replace('"', '＂'),
                str(i[6]).replace('"','＂'))

    ce=cursor.execute(sql_insert)
    conn.commit()
    j += 1
    print('EI：', ce,'No：', j)

cursor.close()
conn.close()