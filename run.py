import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
import math

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')
SANDWICH_TYPES = SHEET.worksheet('stock').get_all_values()[0]



def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    update_worksheet(sales_data, 'sales')
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_worksheet(data, worksheet_name):
    """
    Update worksheet, add new row with the list data provided.
    """
    print(f"Updating {worksheet_name} worksheet...\n")
    worksheet = SHEET.worksheet(worksheet_name)
    worksheet.append_row(data)
    print(f"{worksheet_name} worksheet updated successfully.\n")

def calculate_surplus(sales):
    """
    Source the last stock from previous day.
    """
    stock_data = SHEET.worksheet('stock').get_all_values()
    previous_stock = stock_data[-1]
    stock = [int(value) for value in previous_stock]

    surplus_data = [] 

    for item, sale in zip(stock, sales):
        surplus_data.append(int(item) - int(sale))
    
    update_worksheet(surplus_data, 'surplus')
    return surplus_data
   
def get_last_5_entries_sales(columns):
    """
    Collect data for last five sales tally for each menu item
    converts to integer and returns columns as lists
    """
    print("Collecting stocks data...\n")
    column_matrix = []
    for i in range(1, columns + 1):
        sales_data = SHEET.worksheet('sales')
        sales_columns = sales_data.col_values(i)[-5:]
        sales_column_converted = [int(x) for x in sales_columns]
        column_matrix.append((sales_column_converted))

    return column_matrix
        
def stock_recommendation(sales):
    print("Calculating stock recommendations...\n")
    recommendation = []
    for category in sales:
        recommendation.append(round((sum(category) / len(category)) * 1.1))

    update_worksheet(recommendation, 'stock')
    return recommendation


# 10,20,30,10,20,30

def main():
    data = get_sales_data()
    calculate_surplus(data)
    sales = get_last_5_entries_sales(len(SANDWICH_TYPES))
    stock_recommendation(sales)

print("\nWelcome to Love Sandwiches stock management!\n")

main()
