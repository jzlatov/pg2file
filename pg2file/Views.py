from sqlalchemy.engine import create_engine
from sqlalchemy.sql.expression import text
import os
from pg2file.SqlStrings import PG_CONN_STR

SQL_VIEWS='''
SELECT v.schemaname, v.viewname, pg_get_viewdef(c.oid, True)
FROM pg_views v
inner join pg_catalog.pg_class c on c.relname=v.viewname
WHERE v.schemaname NOT IN ('pg_catalog', 'information_schema')
'''

def GetViews(host, database, user, password):
    try:
        connection_string = PG_CONN_STR.format(hostName=host, dbName=database, userName=user, password=password )
        conn = create_engine(connection_string, client_encoding='utf8').engine.connect()
        views = conn.execute(text(SQL_VIEWS)).fetchall()
        return views
    except Exception:
        raise
    finally:
        conn.close()
        

def WriteViews(path, host, db, user, password):
    functions = GetViews(host=host, 
                        database=db, 
                        user=user, 
                        password=password)
    for function in functions:
        path_out = os.path.join(path, function[0], 'views', function[1] + '.sql')
        if not os.path.exists(os.path.dirname(path_out)):
            os.makedirs(os.path.dirname(path_out))
        print path_out
        f = open(path_out, 'w')
        try:
            f.write(function[2])
        finally:
            f.close()