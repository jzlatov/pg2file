from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import String
import sqlalchemy.types as types

class tsvector(types.UserDefinedType):
    __visit_name__ = "user_defined"
    def __init__(self):
        pass
    
    def get_col_spec(self):
        return "tsvector"

    def bind_processor(self, dialect):
        def process(value):
            return str(value)
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value
        return process

class tsquery(types.UserDefinedType):
    __visit_name__ = "user_defined"
    def __init__(self):
        pass
    
    def get_col_spec(self):
        return "tsquery"

    def bind_processor(self, dialect):
        def process(value):
            return str(value)
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value
        return process    
from sqlalchemy.dialects.postgresql.base import ischema_names
ischema_names['tsvector'] = tsvector
ischema_names['tsquery'] = tsquery
