# Voice-Based-E-Mail
This is a Python Application which allows its users to send, receive E-Mails through voice.


Prerequisites:-
   1. Python 3
   2. The pipenv package management tool.
   3. Access to the internet and a web browser.
   4. A Google account with Gmail enabled.
   
   Use the link given to create client_secret.json
   https://developers.google.com/gmail/api/quickstart/python
   
- Obtain credentials for Google Cloud TTS and Speech Recognization services:
  - You will need to create a google cloud service account with no role and export it's credentials as JSON to a file called
    `api_key.json` under `secrets`.
  - Run `export GOOGLE_APPLICATION_CREDENTIALS=secrets/api_key.json` to activate the API key
  - Alternatively add `GOOGLE_APPLICATION_CREDENTIALS=secrets/api_key.json` to a `.env` file to automatically load it during    Pipenv startup
- Install dependencies using `pipenv install`
- Start Pipenv shell with `pipenv shell`
- Run `python -m voicemail.main`
