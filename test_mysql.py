import pymysql

try:

    conn = pymysql.connect(
        host="62.149.150.167",
        user="Sql589628",
        password="a8dd9c53",
        database="Sql589628_5",
        port=3306
    )

    print("CONNESSIONE OK")

    conn.close()

except Exception as e:

    print("ERRORE:")
    print(e)