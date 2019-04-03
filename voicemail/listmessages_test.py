from .authenticate import service
from .voice import TTSEngine
from .listmessages import ListMessagesMatchingQuery, speak_message
from .getmessage import GetMimeMessage

tts = TTSEngine()

print('Lisitng messages...')
maillist = ListMessagesMatchingQuery(service, 'me')
number = 0

messageIDs = []

print('Asssiging IDs')
while number < 10:
    messageIDs.append(maillist[number]['id'])
    number = number + 1

number = 0
senders = []
while number < 10:
    current_message = GetMimeMessage(service, "me", messageIDs[number])
    senders.append(current_message['from'])
    number = number+1

speak_message(messageIDs[0], tts)


