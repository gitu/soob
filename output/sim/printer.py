__author__ = 'flsc'


class PrinterSim():
    def __init__(self):
        pass


    def __getattr__(self, attrname):
        def tmp_func(*args):
            print ("PRINT; ", attrname, args)

        return tmp_func