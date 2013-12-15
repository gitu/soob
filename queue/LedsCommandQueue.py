import SqliteQueue
import ConfigParser

class LedCommandQueue(SqliteQueue):
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read("../config.ini")
        super.__init__(config.get("DB","file"),"led_commands")
