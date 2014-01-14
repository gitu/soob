from binascii import hexlify, unhexlify
from struct import pack


class WLControl():
    def __init__(self, blink_bee, addr, addr_long):
        self.blink_bee = blink_bee
        self.addr = addr
        self.addr_long = addr_long

    def _tx(self, command, data=None):
        cmd = command
        if not data is None:
            cmd = cmd + data
        print "## sending " + hexlify(cmd) + " len: " + str(len(cmd)) + " to node " + hexlify(self.addr_long)
        if not data is None:
            print "   data: " + hexlify(cmd)
        self.blink_bee.send(addr_long=self.addr_long, addr_short=self.addr, expected_confirm_command=command, data=cmd,
                            timeout=20)

    def tx(self, command, data=None):
        self._tx(self._cmd_byte(command),data)

    def _build_data(self, cmd, *args):
        try:
            cmd_spec = self.commands[cmd]
        except AttributeError:
            raise NotImplementedError(
                "API command specifications could not be found; use a derived class which defines 'api_commands'.")

        if len(args)==2 and args[0] == "unhex":
            return unhexlify(args[1])
        elif "hex_pack" in cmd_spec:
            hex_arg = args[0].decode('hex')
            return pack(cmd_spec["hex_pack"], *hex_arg)
        elif "pack" in cmd_spec:
            return pack(cmd_spec["pack"], *args)
        else:
            return None

    def _cmd_byte(self, cmd):
        try:
            cmd_spec = self.commands[cmd]
        except AttributeError:
            raise NotImplementedError(
                "API command specifications could not be found; use a derived class which defines 'api_commands'.")
        return cmd_spec["cmd_byte"]

    def send(self, cmd, *args):
        self._tx(self._cmd_byte(cmd), self._build_data(cmd, *args))

    def __getattr__(self, name):
        if name == 'commands':
            raise NotImplementedError(
                "API command specifications could not be found; use a derived class which defines 'api_commands'.")

        if name in self.commands:
            return lambda *args: self.send(name, *args)
        else:
            raise AttributeError("XBee has no attribute '%s'" % name)