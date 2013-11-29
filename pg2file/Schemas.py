SQL_SCHEMAS="""select * from information_schema.schemata where schema_name not in ('pg_catalog', 'information_schema') and schema_name not like 'pg_toast%' and and schema_name not like 'pg_temp%';"""

def GetSchemas(conn):
    try:
        cur = conn.cursor()
        cur.execute(SQL_SCHEMAS)
        functions = cur.fetchall()
        conn.commit()
        return functions
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()