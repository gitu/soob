from SqliteQueue import SqliteQueue
import ConfigParser

def make_led_queue():
    config = ConfigParser.ConfigParser()
    config.read("../config.ini")
    path = config.get("DB","file")
    q = SqliteQueue(path,"led_commands")
    return q