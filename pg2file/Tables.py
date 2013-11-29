
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData, CreateTable, CreateIndex
from sqlalchemy.sql.expression import text
import os
from pg2file.SqlStrings import PG_CONN_STR

SQL_TABLE_TRIGGERS='''
SELECT c.oid,c.relname, pg_get_triggerdef(tr.oid) as "trigger"
FROM pg_catalog.pg_class c
    LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
    INNER JOIN pg_catalog.pg_trigger tr ON (tr.tgisinternal = False AND tr.tgrelid = c.oid)
WHERE (pg_catalog.pg_table_is_visible(c.oid))
    AND c.relname = '{TableName}' 
AND c.relkind in ('r','v')
'''

SQL_TABLE_COMMENT='''
SELECT c.oid,c.relname, obj_description(c.oid) as "comment"
FROM pg_catalog.pg_class c
    LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
WHERE (pg_catalog.pg_table_is_visible(c.oid))
    AND c.relname = '{TableName}' 
AND c.relkind in ('r','v')
'''

SQL_COMMENT_ON_TABLE="""COMMENT ON TABLE {Schema}."{TableName}" IS '{Comment}'"""

def GetTables(host, database, user, password, schema='public'):
    connection_string = PG_CONN_STR.format(hostName=host, dbName=database, userName=user, password=password )
    engine = create_engine(connection_string, client_encoding='utf8')
    conn = engine.connect()
    metadata = MetaData(bind=engine, schema=schema)
    metadata.reflect(bind=engine)
    tables = []
    for table in metadata.sorted_tables:
        # create table
        sql =  str(CreateTable(table, bind=engine)).strip() + ';\n'
        # comment on table
        comment = conn.execute(text(SQL_TABLE_COMMENT.format(TableName=table.name))).fetchall()
        sql += (SQL_COMMENT_ON_TABLE.format(Schema=table.schema,TableName=table.name,Comment=comment[0][2]) + ';\n') if comment[0][2] else '' 
        # create indexes
        sorted_indexes = sorted(table.indexes, key=lambda ind: ind.name)
        for index in sorted_indexes:
            sql += str(CreateIndex(index, bind=engine)) + ';\n'
        # create triggers
        triggers = conn.execute(text(SQL_TABLE_TRIGGERS.format(TableName=table.name))).fetchall()
        for trigger in triggers:
            sql += trigger[2] + ';\n'
        tables.append((table.schema, table.name,sql))
    return tables

def WriteTables(path, host, db, user, password):
    tables = GetTables(host, db, user, password, 'contrib')
    tables += GetTables(host, db, user, password, 'public')
    for table in tables:
        path_out = os.path.join(path, table[0], 'tables', table[1] + '.sql')
        if not os.path.exists(os.path.dirname(path_out)):
            os.makedirs(os.path.dirname(path_out))
        print path_out
        f = open(path_out, 'w')
        try:
            f.write(table[2])
        finally:
            f.close()