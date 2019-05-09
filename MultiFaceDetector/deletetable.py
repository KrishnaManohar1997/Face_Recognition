import mysql.connector as mysql
from mysql.connector import Error
DB_NAME = "9JRQMmVx9k"
SqlDB = mysql.connect(
    host = "remotemysql.com",
    port = "3306",
    user = "9JRQMmVx9k",
    password = "RWiVc5LET0",
    database = DB_NAME,
    use_pure = True
    )
cursor = SqlDB.cursor()
cursor.execute("DROP TABLE EmployeeFaceEncodings")
cursor.commit()
cursor.close()
SQLdB.close()