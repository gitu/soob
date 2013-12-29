import SqliteQueue
import ConfigParser

def make_print_queue():
    config = ConfigParser.ConfigParser()
    config.read("../config.ini")
    path = config.get("DB","file")
    q = SqliteQueue(path,"print_commands")
    return q
