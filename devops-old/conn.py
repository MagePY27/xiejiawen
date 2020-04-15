import MySQLdb

conn= MySQLdb.connect(
    host='192.168.99.105',
    port = 3306,
    user='python',
    passwd='aaa',
    db ='devops',
)
cur = conn.cursor()
print(cur)