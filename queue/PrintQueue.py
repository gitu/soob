import SqliteQueue
import ConfigParser

class PrintQueue(SqliteQueue):
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read("../config.ini")
        super.__init__(config.get("DB","file"),"print_commands")
