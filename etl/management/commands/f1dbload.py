from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import gzip
import MySQLdb as mysql
import re

import f1_stats.db_settings as f1db

class Command(BaseCommand):

    help = 'Loads new MySQL dump into f1db'

    def handle(self, *args, **options):

        def mysql_conn_etl(dbName):
            db = mysql.connect(f1db.DB_HOST, f1db.DB_ETL_USER, f1db.DB_ETL_USER_PASSWORD, dbName)
            return db


        def mysql_execute(cursor, statement):
            try:
                cursor.execute(statement)

            except Exception as e:
                print(e)
                print(statement)



        def mysql_sql_from_file(fHandler, cursor):
            statement = ''.encode('utf-8')
            for sql in fHandler:
                if sql != '\n' and sql[:2] != '--':
                    if not re.search(r'[^-;]+;', sql):
                        statement += sql.encode('utf-8')
                    else:
                        statement += sql.encode('utf-8')
                        mysql_execute(cursor, statement)
                        statement = ''.encode('utf-8')
                        
                        # try:
                        #     cursor.execute(statement)
                        #     statement = ''.encode('utf-8')

                        # except Exception as e:
                        #     print(e)
                        #     print(sql)


        def f1db_load_dump():
            db = mysql_conn_etl(f1db.DB_NAME)
            cursor = db.cursor()

            f = gzip.open(f1db.DB_DUMP_PATH, 'rt')
            mysql_sql_from_file(f, cursor)

            f.close()
            db.close()


        def f1db_update_stats():
            db = mysql_conn_etl(f1db.DB_NAME)
            cursor = db.cursor()

            sql = 'CALL f1db.updateDriverStats'
            mysql_execute(cursor, sql)

            db.close()



        f1db_load_dump()
        f1db_update_stats()