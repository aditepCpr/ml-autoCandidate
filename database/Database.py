import mysql.connector as mariadb
from sys import platform

def conn():
    if platform == "win32":
        mariadb_connection = mariadb.connect(host="192.168.1.2", user='doae', password='1234', database='doae_dev')
    else:
        mariadb_connection = mariadb.connect(host="192.168.1.2", user='doae', password='1234',
                                             database='doae_dev')
    return mariadb_connection
