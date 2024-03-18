import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT=gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

sales = SHEET.worksheet('sales')

def get_sales_values():
    """ 
    Get sales data input from the user
    """

    while True:
        print("Please enter the sales data from the last market")
        print("Data should be six numbers, separated by commas")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        values = data_str.split(',')

        validate_data(values)
        if validate_data(values) == True:
            print("The data is valid")
            break



def validate_data(values):
    """
    Makes sure the user input is valid and can be manipulated later
    """

    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                 f"You provided {len(values)} values. 6 are required, please try again.")
        return True
    except ValueError as e:
        print(f"Input error: {e}")
    return False


data = get_sales_values()      