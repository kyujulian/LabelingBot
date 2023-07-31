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

def update_values(spreadsheet_id, range_name, value_input_option, _values):

    for value in _values:
        if value[1] == constants.ENDTOKEN:
            value[1] = ""
            
    try:
        service = build('sheets', 'v4', credentials=constants.CREDS)
        body = {
            "values" : _values
        }

        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body
        ).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))
        return result
    except HttpError as error:
        print(f"An error occured: {error}")
        return error


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
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    validateToken(constants.CREDS,constants.SCOPES)

    sheet = Sheet(constants.SPREADSHEET_ID, range_values="Sheet1")
    # print(sheet.data)
    # sheet.update_with_class()

    print("running bot");

    bot.run(sheet)

if __name__ == "__main__":
    main()
