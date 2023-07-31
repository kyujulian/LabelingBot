# Helpers
from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests import HTTPError

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

            columns, read_values = self.parse_input(read_values)


            if not(read_values):
                print("No data found.")
                return

            print("COLUMNS")
            print(columns)
            print(read_values)

            self.columns = columns
            self.data = read_values
            self.range = range_values
            self.sheet_id = sheet_id

        except HttpError as err:
            print(err)
    def sort(self,range_values="Sheet1"):
        print("Sorting values on sheets")
        #FIX row length
        self.data[1:].sort(key=lambda x: x['class'])
        try:
            self.update_values(self.parse_for_output(),range_values=range_values)

        except HTTPError as err:
            print(err)


            
    def parse_input(self,data):

        columns = data[0]

        err_counter = 0
        for row in data[1:]:
            #FIX row length
            if len(row) < 2:
                row.append(constants.ENDTOKEN)

            elif row[-1] not in constants.CLASSES:
                row[-1] = constants.ENDTOKEN

            elif (len(row) > constants.MAXCOL):
                raise Exception(f"""
                                Sheet misconfigured, error in row {err_counter} \n
                                row was expected to have  {constants.MAXCOL} columns, it has {len(row)}
                                """)
            
            err_counter +=1
        
        list_of_dicts = []
        for row in data[1:]:
            new_row = {columns[i] : row[i] for i in range(len(row))}
            list_of_dicts.append(new_row);

        return (columns, list_of_dicts)
        
    def parse_for_output(self):
        list_of_lists = [self.columns]
        list_of_lists += [ [d[column] for column in self.columns] for d in self.data]

        return list_of_lists

        
    def add_and_write(self, tweet, classification, range_values="Sheet2"):
        row = {self.columns[0]: tweet, self.columns[1]: classification}
        self.data.append(row)
        self.update_with_class()
    
    def get_unclassified(self):
        unclass_data = self.get_data_without_class()
        return unclass_data[0][self.columns[0]]

    def get_data_without_class(self):

        new_data = []

        for row in self.data:
            if row['class'] == constants.ENDTOKEN:
                new_data.append(row)

        return new_data
    
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
