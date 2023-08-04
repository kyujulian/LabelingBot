from __future__ import print_function

import os.path
import constants
import bot

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from api import Sheet

def validateToken(creds, scopes):
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

def main():
    global CREDS

    

    if not os.path.exists(constants.DATA_DIR):
        os.makedirs(constants.DATA_DIR)


    validateToken(constants.CREDS,constants.SCOPES)

    sheet = Sheet(constants.SPREADSHEET_ID, range_values=constants.SPREADHSHEET_PAGE)

    print("running bot");

    bot.run(sheet)

if __name__ == "__main__":
    main()
