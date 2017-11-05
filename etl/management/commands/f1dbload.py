from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import gzip
import MySQLdb as mysql
import re
import sys
sys.path.append(R'/home/max/Documents/python/project/f1_stats/')
from conf import conf


class Command(BaseCommand):

    help = 'Loads new MySQL dump into f1db'

    def handle(self, *args, **options):

        def mysql_conn_etl(dbName):
            db = mysql.connect(conf.DB_HOST, conf.DB_USER, conf.DB_USER_PASSWORD, dbName)
            return db


        def mysql_sql_from_file(fHandler, cursor):
            statement = ''.encode('utf-8')
            for sql in fHandler:
                if sql != '\n' and sql[:2] != '--':
                    if not re.search(r'[^-;]+;', sql):
                        statement += sql.encode('utf-8')
                    else:
                        statement += sql.encode('utf-8')
                        try:
                            cursor.execute(statement)
                            statement = ''.encode('utf-8')

                        except Exception as e:
                            print(e)
                            print(sql)


        def f1db_load_dump():
            db = mysql_conn_etl(conf.DB_NAME)
            cursor = db.cursor()

            f = gzip.open(conf.DB_DUMP_PATH, 'rt')
            mysql_sql_from_file(f, cursor)

            f.close()
            db.close()


        f1db_load_dump()