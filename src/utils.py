from requests import HTTPError
import constants
import api

def sort(data, spreadsheet_id = constants.SPREADSHEET_ID, range_name = "Sheet1"):
    print("Sorting values on sheets");
    #FIX row length
    data.sort(key=lambda x: x[1])
    try:
        api.update_values(spreadsheet_id, range_name, "USER_ENTERED", data)
    except HTTPError as err:
        print(err)


def validate_input(data):

    counter = 0
    for row in data:
        #FIX row length
        if len(row) < 2:
            row.append(constants.ENDTOKEN)
        elif row[-1] not in constants.CLASSES:
            row[-1] = constants.ENDTOKEN

        elif (len(row) > constants.MAXCOL):
            raise Exception(f"""
                            Sheet misconfigured, error in row {counter} \n
                            row was expected to have  {constants.MAXCOL} columns, it has {len(row)}
                            """)
        
        counter +=1