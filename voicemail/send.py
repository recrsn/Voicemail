#!/usr/bin/env python3
# Requires PyAudio and PySpeech.


import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from fuzzywuzzy import process

from googleapiclient import errors

from .authenticate import service
from .voice import speech_to_text


def create_message(sender, to, subject, message_text, attachments):

    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    for path in attachments:
        content_type, encoding = mimetypes.guess_type(path)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        with open(path, 'rb') as fp:
            if main_type == 'text':
                msg = MIMEText(fp.read(), _subtype=sub_type)
            elif main_type == 'image':
                msg = MIMEImage(fp.read(), _subtype=sub_type)
            elif main_type == 'audio':
                msg = MIMEAudio(fp.read(), _subtype=sub_type)
            else:
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(fp.read())

        filename = os.path.basename(path)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_string())}


def send_message(tts):
    tts.speak('say the E-Mail address of the receiver')
    email = speech_to_text()
    words = email.split()
    modified_mail = str()
    for word in words:
        if word == 'underscore':
            modified_mail = modified_mail+'_'
        elif word == 'dot':
            modified_mail = modified_mail+'.'
        else:
            modified_mail = modified_mail+word

    modified_mail = modified_mail.lower()
    print(modified_mail)
    to = modified_mail
    tts.speak('say the subject of the message you want to send !')
    subject = speech_to_text()
    tts.speak('say the message you want to send !')
    message_text = speech_to_text()

    attachments = []

    tts.speak('Do you want to add any attachments ?')
    response = speech_to_text()
    if response.lower() == 'yes':
        while True:
            tts.speak(
                'Where is your file located in? Documents, Music, Pictures or Desktop?')
            directory = speech_to_text()

            if directory.lower() not in ['documents', 'music', 'pictures', 'desktop']:
                tts.speak('Directory not recognized')
                continue

            folder = os.path.join('~', directory.capitalize())

            tts.speak('Which file do you want to send?')
            file_name = speech_to_text()
            selected_file = process.extractOne(file_name, os.listdir(folder))
            attachments.append(os.path.join(folder, selected_file))

            tts.speak('Do you want to add more attachments?')
            response = speech_to_text()

            if response != 'yes':
                break

    created_message = create_message(
        'me', to, subject, message_text, attachments)
    try:
        message = (service.users().messages().send(userId='me', body=create_message)
                   .execute())
        print('Message Id: %s' % message['id'])
        print(message)
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
