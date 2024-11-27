import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ========================
# Load and parse the data
# ========================

# Load the CSV data  and store it in a DataFrame

# [PRINT THE DATAFRAME TO SEE THE DATA]
dataFrame = pd.read_csv('data.csv')

# Looping over 4 columns 
for col in ['Close/Last', 'Open', 'High', 'Low']:
    # Accessing specific columns using col 
    # replacing the dollar sign and then converting the string into float 
    # We need to replace the dollar sign because if we store it as a string, we can't do math operations on it, so we need to store it as a float or int, and 
    # if we have a dollar sign, it will cause an error 
    dataFrame[col] = dataFrame[col].str.replace('$', '').astype(float)

# Changing the date column to datetime format -- compare to excel date format, currently the date is in "general" format
dataFrame['Date'] = pd.to_datetime(dataFrame['Date'])

# Sort by company and date
dataFrame = dataFrame.sort_values(by=["Company", "Date"])

# ========================
# Calculate monthly percentage change
# ========================

# Add a new column for the month
dataFrame['Month'] = dataFrame['Date'].dt.to_period('M')

# Group by company and month, and get the last row for each month
monthlyFrame = dataFrame.groupby(['Company', 'Month']).last()

# go through each company
for company, group in monthlyFrame.groupby('Company'):
    print(f"\n{company}")

    # Include december of last year to calculate percentage change for january
    months = ['2021-12', '2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06', '2022-07', '2022-08', '2022-09', '2022-10', '2022-11', '2022-12']
    # Names for prettier output
    names = ['Dec 2021', 'Jan 2022', 'Feb 2022', 'Mar 2022', 'Apr 2022', 'May 2022', 'Jun 2022', 'Jul 2022', 'Aug 2022', 'Sep 2022', 'Oct 2022', 'Nov 2022', 'Dec 2022']

    # Start at january
    for i in range(1, len(months)):

        # last months close price
        first_close = monthlyFrame.loc[(company, months[i-1]), 'Close/Last']
        # this months close price
        last_close = monthlyFrame.loc[(company, months[i]), 'Close/Last']

        # calculate percentage change
        percentage_change = ((last_close - first_close) / first_close) * 100
        print(f"{names[i]} : {percentage_change:.2f}%")

    # yearly percentage change
    first_close = monthlyFrame.loc[(company, '2021-12'), 'Close/Last']
    last_close = monthlyFrame.loc[(company, '2022-12'), 'Close/Last']
    percentage_change = ((last_close - first_close) / first_close) * 100
    print(f"Yearly: {percentage_change:.2f}%")


# We only want to analyze the year of 2022, so we are filtering the data to only include the year 2022
# & condition so both conditions must be true 
# We need the dataframe so we actually select and filter the rows 
dataFrame = dataFrame[(dataFrame['Date'] >= '2022-01-01') & (dataFrame['Date'] <= '2023-01-01')]

# Creates a new empty dataframe for the normalized data 
performance = pd.DataFrame()

# For loop that splits DataFrame into groups based on unique values in the Company column 
# since there are 10 unique companies, we will create 10 groups, and we will iterate over each group 
# "stock" holds the name of the company 
for ticker, group in dataFrame.groupby('Company'):
    
    # Sort the date in chronological order based on date column 
    group = group.sort_values('Date')
    
    # Finds the intial price of the stock 
    #
    initial_price = group.loc[group['Date'] == group['Date'].min(), 'Close/Last'].iloc[0]
    
    
    group['investment_value'] = (group['Close/Last'] / initial_price) * 1000
    
    # Add to performance DataFrame
    performance[ticker] = group.set_index('Date')['investment_value']


# ========================
# Create chart for performance in 2022
# ========================

# Plot the performance
performance.plot(figsize=(12, 6), title='Performance of $1000 Investment (2022-2023)')

# Customize x-axis
plt.xlabel('Month')
plt.ylabel('Investment Value ($)')

# Set month spacing and format the dates
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Spacing the months
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Formatting as 'YYYY-MM'

# Place legend outside the plot
plt.legend(title='Company', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.grid(True)

plt.tight_layout()  # Adjust layout to fit everything
plt.show()