version = "0.0.1"
from Tables import WriteTables
from Functions import WriteFunctions
from TriggerFunctions import WriteTriggerFunctions
from Views import WriteViews
from Types import WriteTypes

def WriteAll(host, db, user, password, path):
    WriteTables(path, host, db, user, password)
    WriteFunctions(path, host, db, user, password)
    WriteTriggerFunctions(path, host, db, user, password)
    WriteViews(path, host, db, user, password)
    WriteTypes(path, host, db, user, password)
