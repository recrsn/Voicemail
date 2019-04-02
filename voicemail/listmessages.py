#!/usr/bin/env python3
# Requires PyAudio and PySpeech.


"""Get a list of Messages from the user's mailbox.
"""
from .voice import speech_to_text
from googleapiclient import errors
from .authenticate import *
from .getmessage import *
import html2text
import pyttsx3


def ListMessagesMatchingQuery(service, user_id, query=''):
    """List all Messages of the user's mailbox matching the query.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      query: String used to filter messages returned.
      Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
      List of Messages that match the criteria of the query. Note that the
      returned list contains Message IDs, you must use get with the
      appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id,
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def ListMessagesWithLabels(service, user_id, label_ids=[]):
    """List all Messages of the user's mailbox with label_ids applied.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      label_ids: Only return Messages with these labelIds applied.

    Returns:
      List of Messages that have all required Labels applied. Note that the
      returned list contains Message IDs, you must use get with the
      appropriate id to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id,
                                                   labelIds=label_ids).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id,
                                                       labelIds=label_ids,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def speak_message(msg_id, tts):
    message = GetMimeMessage(service, "me", msg_id)
    a = message.get_payload()
    b = a[0].get_payload()
    print(type(b))
    tts.speak('The subject is : ')
    tts.speak(message['subject'])
    print(b)
    tts.speak('The message is : ')
    tts.speak(b)


def searched_message(query, tts):
    number = 0
    searched_message_list = ListMessagesMatchingQuery(
        service, 'me', 'from:'+query)
    searched_messageIDs = list()
    while number < len(searched_message_list):
        searched_messageIDs.append(searched_message_list[number]['id'])
        number = number+1
    subjects = list()
    for current_mailID in searched_messageIDs:
        searched_message = GetMimeMessage(service, "me", current_mailID)
        subjects.append(searched_message['subject'])

    number = 0
    for subject in subjects:
        tts.speak(str(number)+' '+subject)
        number = number+1
    if len(subjects) == 0:
        tts.speak('No E-Mails from this sender!')
        return
    response = speech_to_text()
    # message=GetMimeMessage(service,'me',searched_messageIDs[int(response)])
    speak_message(searched_messageIDs[int(response)], tts)


def get_message_list(tts):

    maillist = ListMessagesMatchingQuery(service, 'me')

    number = 0

    messageIDs = list()
    while number < 100:
        messageIDs.append(maillist[number]['id'])
        number = number + 1

    number = 0
    senders = list()
    while number < 100:
        current_message = GetMimeMessage(service, "me", messageIDs[number])
        senders.append(current_message['from'])
        number = number+1

    number = 0
    while True:
        tts.speak('Say the serial number of E-Mail to read !')
        # number=0
        # while number < 10 :
        while True:
            tts.speak(str(number)+' '+senders[number])
            # number=number+1
            if number % 10 == 9:
                # number=number+1
                break
            number = number+1

        tts.speak('say next to hear next ten messages')
        tts.speak('say skip to return to the main menu')

        response = speech_to_text()
        if response.lower() == 'skip':
            return
        # response=int(response)
        if response.lower() == 'next':
            number = number+1
            continue
        response = int(response)

        speak_message(messageIDs[response], tts)

        tts.speak('say continue to hear the E-Mails again !')
        response = speech_to_text()
        if response.lower() == 'continue':
            number = number-10
            continue
