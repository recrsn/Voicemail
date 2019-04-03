from .voice import TTSEngine, speech_to_text
from .send import send_message
from .listmessages import get_message_list, searched_message


def main():

    tts = TTSEngine()

    while True:

        tts.speak('say 1 to send a message !')
        tts.speak('say 2 to receive messages !')
        tts.speak('say 3 to close the application !')

        first_response = speech_to_text()

        if first_response == '1':
            print('Getting ready to compose message...')
            send_message(tts)

        elif first_response.lower() in ['2', 'tu', 'two', 'to']:
            tts.speak('say 1 for top ten messages')
            tts.speak('say 2 to search for a sender')
            receive_response = speech_to_text()

            if receive_response.lower() in ['1', 'one']:
                print('Showing top 10 messages...')
                get_message_list(tts)
            elif receive_response.lower() in ['2', 'tu', 'two', 'to']:
                tts.speak('Say the E-Mail of the sender!')
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
                query = speech_to_text()
                print('search message')
                searched_message(modified_mail, tts)
            elif first_response == '3':
                exit()
        else:
            tts.speak('Sorry you were not clear with your vocals !')
            continue


if __name__ == "__main__":
    main()
