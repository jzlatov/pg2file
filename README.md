pg2file
=======


Utility for simple saving postgresql database schema(without data) to separated files in folders structure.

**Potential use-case scenarios**:
* Version control your database schema.
* Compare differences of schema dumps created in different points in time. Since objects are stored in separate files, it is easier to see what areas were modified, compared to looking at the diff of two entire schemas.
* Restore only some objects, based on type (e.g., only the functions) or name (e.g. only fucntions of certain name/names).

#Directories tree

    --20131128_1816                 <--- timestamp folder only with --timestamp option
        `-- localhost               <--- host name
            `-- siw                 <--- database name
                |-- contrib         <--- schema name
                |   `-- functions
                |       `-- generate_dates(date,date,integer).sql
                `-- public
                    |-- functions
                    |-- tables
                    |   `-- User.sql
                    `-- types
                        `-- user_row.sql

#Installation

**Prerequisites**:
* [Python 2.7 (tested only with this version) ](http://python.org/ "Python") 
* [SqlAlchemy](ttp://www.sqlalchemy.org/ "SqlAlchemy") 
* [psycopg2 ](http://initd.org/psycopg/ "psycopg2") 

**Installation**:

    python setup.py install


#Usage
    usage: runpg2file [-h] [--port [PORT]] [--timestamp]
                      [host] [database] [user] [password] [path]
    
    Utility for simple saving postgresql database schema(without data) to separated files
    in folders structure.
    
    positional arguments:
      host           Database host
      database       Database name
      user           Database user name
      password       Database user password
      path           Output directory
    
    optional arguments:
      -h, --help     show this help message and exit
      --port [PORT]  Database port
      --timestamp    Add first folder with timestamp name


##Example usage

    runpg2file localhost my_database_name my_db_user my_password /tmp/backups/ --port=6432 --timestamp

or without install go to scrits/ folder and run  

    python runpg2file localhost my_database_name my_db_user my_password /tmp/backups/ --port=6432 --timestamp

#List of currently supported database objects:  

* Tables (indexes and constraints included)
* Views
* Types
* Functions
* Trigger functions

    **NOTE 1**
   For functions with long name (with long list of parameters, with length > 255) will be used unique specific_name from information_schema.routines like "FunctionName-1234"

    **NOTE 2**
    Only public and contrib schemas are exported

#TODO

* schemas choice
* add support for object types:
  * Schemas
  * Sequences
  * Procedural languages
  * Aggregates



