from __future__ import unicode_literals

from imapclient import IMAPClient
import email


ssl = True

server = IMAPClient(HOST, port=993, use_uid=True, ssl=ssl)

print server.capabilities()

server.login(USERNAME, PASSWORD)

select_info = server.select_folder('INBOX')
print('%d messages in INBOX' % select_info['EXISTS'])

print("Messages:")
messages = server.search(['NOT DELETED'])
response = server.fetch(messages, ['RFC822', ])
for msgid, data in response.iteritems():
    msg = email.message_from_string(data['RFC822'])
    payload = msg.get_payload(None, True)
    print 'From: %s' % msg['from']
    print 'Subject: %s' % msg['subject']
    print  payload



server.idle()

x = 1
while x < 10:
    responses = server.idle_check(timeout=200)
    x += 1
    if [i for i, v in enumerate(responses) if v[1] == u'EXISTS']:
        print "will fetch new messages"
        server.idle_done()
        new_messages = server.search(NEW_MSG_CRITERIA)
        response = server.fetch(new_messages, ['FLAGS', 'RFC822.SIZE', 'BODY[HEADER.FIELDS (SUBJECT)]', 'BODY[TEXT]', ])
        for msgid, data in response.iteritems():
            print(msgid)
            print data['BODY[HEADER.FIELDS (SUBJECT)]']
            print "body: ", data['BODY[TEXT]']
        server.idle()
    else:
        print [x[1] for x in responses]

# Come out of IDLE mode
text, responses = server.idle_done()
print('IDLE done. Server said %r' % text)
print('Final responses: ', responses)

print(server.logout())