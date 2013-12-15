import ConfigParser
from imapclient import IMAPClient
import email
import json
import logging
from queue import LedCommandQueue

ssl = True

config = ConfigParser.ConfigParser()
config.read("../config.ini")

HOST = config.get("Mail","imap_host")
USERNAME = config.get("Mail","imap_user")
PASSWORD = config.get("Mail","imap_pass")
NEW_MSG_CRITERIA = ['NOT DELETED', 'UNSEEN', 'FROM '+config.get("Mail","From")]

led_queue = LedCommandQueue()

def set_led(payload):
    try:
        logging.debug("parsing set led")
        commands = json.loads(payload)
        logging.debug(commands)
        for command in commands:
            if command["action"] in ("set_big", "set_ring"):
                led_queue.append(command)
    except Exception, ex:
        logging.exception("Something awful happened while set_led!")


def fetch_new_messages():
    new_messages = server.search(NEW_MSG_CRITERIA)
    response = server.fetch(new_messages, ['RFC822'])
    for msgid, data in response.iteritems():
        msg = email.message_from_string(data['RFC822'])
        logging.debug(u"Payload: " + msg.get_payload(None,True))
        if msg["subject"] == "SET_LED":
            set_led(msg.get_payload(None,True))


while True:
    try:
        server = IMAPClient(HOST, port=993, use_uid=True, ssl=ssl)
        print server.capabilities()
        server.login(USERNAME, PASSWORD)

        select_info = server.select_folder('INBOX')
        logging.debug('%d messages in INBOX' % select_info['EXISTS'])

        while True:
            server.idle()

            try:
                while True:
                    responses = server.idle_check(timeout=200)
                    if [i for i, v in enumerate(responses) if v[1] == u'EXISTS']:
                        logging.debug("will fetch new messages")
                        server.idle_done()
                        fetch_new_messages()
                        server.idle()
                    else:
                        logging.debug("received response: "+ str(responses))
            except Exception, ex:
                logging.exception("error while parsing idle response!")

            text, responses = server.idle_done()
            logging.debug('IDLE done. Server said %r' % text)
            logging.debug('Final responses: ' + str(responses))

            logout_response = server.logout()
            logging.debug('Logout responses: ', logout_response)
    except Exception, ex:
        logging.exception("Something awful happened!")
