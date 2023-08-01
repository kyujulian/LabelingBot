# Helpers
from __future__ import print_function

import os.path


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests import HTTPError

import pandas as pd
import numpy as np


#locals
import constants


class Sheet:

    def __init__(
        self,
        sheet_id,
        range_values
    ):
        try:
            service = build("sheets", "v4", credentials=constants.CREDS)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=sheet_id,
                                        range=range_values).execute()
            read_values = result.get("values", [])

            columns, read_values = read_values[0], read_values[1:]


            if not(read_values):
                print("No data found.")
                return

            print("COLUMNS")
            print(columns)
            print(read_values)

            self.columns = columns
            self.data = pd.DataFrame(columns=columns, data=read_values)
            self.data[constants.CLASSCOL]  = self.data[constants.CLASSCOL].fillna(constants.ENDTOKEN)

            condition = self.data[constants.CLASSCOL].isin(constants.CLASSES) 

            self.data[constants.CLASSCOL] = self.data[constants.CLASSCOL].where(condition, constants.ENDTOKEN)


            self.range = range_values
            self.sheet_id = sheet_id

        except HttpError as err:
            print(err)

    def sort(self,range_values="Sheet1"):
        self.data.sort_values(by=['class'],inplace=True)
        print("Sorting values on sheets")
        try:
            self.update_values(self.parse_for_output(),range_values=range_values)
        except HTTPError as err:
            print(err)


            
    def parse_output(self):
        output = [self.columns] + self.data.to_numpy()
        return output
        
    def add_and_write(self, tweet, classification, range_values="Sheet1"):
        tweet_row = self.data.loc[self.data[constants.TWEETCOL == tweet]]
        print(tweet_row)
        tweet_row['class'] = classification

    
    def get_unclassified(self):
        unclass_data = self.get_data_without_class()
        return unclass_data[0][self.columns[0]]

    def get_data_without_class(self):
        return self.data.loc[self.data['class'] == '']

    
    def filter_classified(self):
        new_data = self.parse_for_output()
        new_data = filter(lambda x: x[-1] != constants.ENDTOKEN, new_data) 
        return new_data
    
    def update_with_class(self):
        new_data = list(self.filter_classified())
        print('NEW DATA')
        print(new_data)
        self.update_values(new_data, range_values="Sheet2")

    def update_values(self,values,range_values="Sheet1",value_input_option="USER_ENTERED"):

        for value in values:
            if value[1] == constants.ENDTOKEN:
                value[1] = ""
                
        try:
            service = build('sheets', 'v4', credentials=constants.CREDS)
            body = {
                "values" : values
            }

            result = service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=range_values,
                valueInputOption=value_input_option,
                body=body
            ).execute()
            print('{0} cells updated.'.format(result.get('updatedCells')))
            return result

        except HttpError as error:
            print(f"An error occured: {error}")
            return error