# Cleaning date range
import datetime


# Variable initialization
name = None
startdate = None
enddate = None

# Request for start date from user
while name is None:
    user_stock = input("Enter a stock: ")
    try:
        # test if user input stock has updated file

    except ValueError:
        print("Encountered an error. Please try again.")

while startdate is None:
    user_start = input("Enter a start date (YYYY-MM-DD): ")
    try:
        # test if user input is valid date format
        startdate = datetime.datetime(int(user_start[0:4]),  # Selected year
                                      int(user_start[5:7]),  # Selected month
                                      int(user_start[8:11]))  # Selected day
    except ValueError:
        print("Invalid start date. Please try again.")

# Request for end date from user
while enddate is None:
    user_end = input("Enter end date (YYYY-MM-DD): ")
    try:
        # test if user input is valid date format
        enddate = datetime.datetime(int(user_end[0:4]),  # Selected year
                                    int(user_end[5:7]),  # Selected month
                                    int(user_end[8:11]))  # Selected day
    except ValueError:
        print("Invalid end date. Please try again.")
