from sqlalchemy.engine import create_engine
from sqlalchemy.sql.expression import text
import os
from pg2file.SqlStrings import PG_CONN_STR
SQL_TYPES='''
SELECT t.oid, n.nspname as "schemaname", format_type(t.oid, null) AS alias, t.typtype, t.typinput, t.typoutput, t.typreceive, t.typsend,
    t.typmodin, t.typmodout, t.typanalyze, t.typispreferred, t.typbyval, t.typdefault, e.typname as element, t.typdelim, t.typlen, t.typcategory, t.typalign,
    t.typstorage, t.typcollation, 
    --pg_get_userbyid(t.typowner) as typeowner,
    description, ct.oid AS taboid, 
    (SELECT array_agg(label) FROM pg_seclabels sl1 WHERE sl1.objoid=t.oid) AS labels,
    (SELECT array_agg(provider) FROM pg_seclabels sl2 WHERE sl2.objoid=t.oid) AS providers,
    (select string_agg('"' || attrs.attname || '" ' ||  attrs.typname, E',\n') from 
        ( SELECT att.attname, 
            format_type(t1.oid,NULL) AS typname, att.attndims, att.atttypmod,  nsp.nspname, (SELECT COUNT(1) from pg_type t2 WHERE t2.typname=t1.typname) > 1 AS isdup, collname, nspc.nspname as collnspname
        FROM pg_attribute att
            JOIN pg_type t1 ON t1.oid=att.atttypid
            JOIN pg_namespace nsp ON t1.typnamespace=nsp.oid
            LEFT OUTER JOIN pg_type b ON t1.typelem=b.oid
            LEFT OUTER JOIN pg_collation c ON att.attcollation=c.oid
            LEFT OUTER JOIN pg_namespace nspc ON c.collnamespace=nspc.oid
        WHERE att.attrelid= t.typrelid
        ORDER by att.attnum) as attrs) as attrs,
    t.typrelid
FROM pg_type t
  LEFT OUTER JOIN pg_type e ON e.oid=t.typelem
  LEFT OUTER JOIN pg_class ct ON ct.oid=t.typrelid AND ct.relkind <> 'c'
  LEFT OUTER JOIN pg_description des ON des.objoid=t.oid
  left outer join pg_catalog.pg_namespace n ON n.oid = t.typnamespace
 WHERE 
    t.typtype != 'd' 
    AND t.typname NOT LIKE E'\\\_%' 
    and n.nspname not in ('pg_catalog', 'information_schema')
    and n.nspname not like 'pg_%'
    and ct.oid is null
 ORDER BY "schemaname", t.typname
 '''
 

def GetTypes(host, database, user, password):
    def GetType(row):
        TYPE_COMPOSITE="c"
        TYPE_ENUM="e"
        TYPE_RANGE="r"
        #TYPE_EXTERNAL=''
        ALIGNS = {'c': 'char','s': 'int2','i': 'int4','d': 'double'}
        STORAGES = {'p': 'PLAIN','e': 'EXTERNAL','m': 'MAIN','x': 'EXTENDED'}
        typtype = row['typtype']
        typinput = row['typinput']
        typoutput = row['typoutput']
        typreceive = row['typreceive']
        typsend = row['typsend']
        typmodin = row['typmodin']
        typmodout = row['typmodout']
        typanalyze = row['typanalyze']
        typispreferred = row['typispreferred']
        typbyval = row['typbyval']
        typdefault = row['typdefault']
        element = row['element']
        typdelim = row['typdelim']
        typlen = row['typlen']
        typcategory = row['typcategory']
        typalign = ALIGNS[row['typalign']] if row['typalign'] in ALIGNS else 'unknown' 
        typstorage = STORAGES[row['typstorage']] if row['typstorage'] in ALIGNS else 'unknown' 
        schemaname = row['schemaname']
        typeName =  row['alias']
        isCollatable = row['typcollation'] == 100
        attrs =  row['attrs']
        sql = 'CREATE TYPE {Schema}."{TypeName}"'.format(Schema=schemaname, TypeName=typeName)
        if typtype == TYPE_COMPOSITE:
            sql += " AS\n   ("  + attrs
        elif typtype == TYPE_ENUM:
            raise Exception('TYPE_ENUM not implemented')
    #        sql +=" AS ENUM\n   ("
        elif typtype == TYPE_RANGE:
            raise Exception('TYPE_RANGE not implemented')
    #        sql += " AS RANGE\n   (SUBTYPE=" + rngsubtypestr
        else:
            sql += "\n   (INPUT=" + typinput + ",\n       OUTPUT=" + typoutput
            if typreceive:
                sql += ",\n       RECEIVE=" + typreceive
            if typsend:
                sql += ",\n       SEND=" + typsend
            if typmodin:
                sql += ",\n       TYPMOD_IN=" + typmodin
            if typmodout:
                sql += ",\n       TYPMOD_OUT=" + typmodout
            if typanalyze:
                sql += ",\n       ANALYZE=" + typanalyze
            sql += ",\n       CATEGORY=" + typcategory
            if typispreferred:
                sql += ",\n       PREFERRED=true"
            if typbyval:
                sql += ",\n    PASSEDBYVALUE"
            if typdefault:
                sql += ", DEFAULT=" + typdefault
            if element:
                sql += ",\n       ELEMENT=" + element + ", DELIMITER='" + typdelim + "'"
            sql += ",\n       INTERNALLENGTH=" + str(typlen) + ", ALIGNMENT=" + typalign + ", STORAGE=" + typstorage
            if isCollatable:
                sql += ",\n       COLLATABLE=true"
        sql +=");\n"
        return (schemaname, typeName.replace('"','') ,sql)
    try:
        connection_string = PG_CONN_STR.format(hostName=host, dbName=database, userName=user, password=password )
        conn = create_engine(connection_string, client_encoding='utf8').engine.connect()
        rows = conn.execute(text(SQL_TYPES)).fetchall()
    except Exception:
        raise
    finally:
        conn.close()
    types = []
    for row in rows:
        types.append(GetType(row))
    return types
        

def WriteTypes(path, host, db, user, password):
    
    types = GetTypes(host=host, 
                     database=db, 
                     user=user, 
                     password=password)
    for typ in types:
        path_out = os.path.join(path, typ[0], 'types', typ[1] + '.sql')
        if not os.path.exists(os.path.dirname(path_out)):
            os.makedirs(os.path.dirname(path_out))
        print path_out
        f = open(path_out, 'w')
        try:
            f.write(typ[2])
        finally:
            f.close()