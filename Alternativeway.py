# importing different datasets 
import pandas as pd
import plotly.graph_objects as go  

#Reads the CSV file for data manipulation 
df = pd.read_csv('data.csv')    

#initilizing empty dictionaries 
stocks = {} 
open_dates = {}

#function to parse the data from the csv file 
def parse_data(csv_file): 


    for index, row in df.iterrows(): #iterates each row of the dataset 
            #Extracts stock symbol and the trade date 
            stock_symbol = row['Company'] 
            date = row['Date']

            # adds each unique year to the open_dates dictionary
            year = date.split('/')[2]
            if year not in open_dates:
                open_dates[year] = []

            # create list of market open dates for each year
            if date not in open_dates[year]:
                open_dates[year].append(date)
            
            # Check if the stock symbol exists in stocks dictionary, if not, initialize an empty dictionary for that stock symbol 
            if stock_symbol not in stocks:
                stocks[stock_symbol] = {}

            # Store the data in the dictionary based on the stock symbol and date 
            #We need to replace the dollar sign because if we store it as a string, we can't do math operations on it, so we need to store it as a float or int, and 
            # if we have a dollar sign, it will cause an error 
            stocks[stock_symbol][date] = {
                'close': float(str(row['Close/Last']).replace('$', '')),
                'volume': row['Volume'],
                'open': float(str(row['Open']).replace('$', '')),
                'high': float(str(row['High']).replace('$', '')),
                'low': float(str(row['Low']).replace('$', ''))
            }

    # sort the dates in ascending order
    for dates in open_dates:
        open_dates[dates].sort(key=lambda date: pd.to_datetime(date))

parse_data('data.csv')

'''
Check if the data is parsed correctly 
print(stocks['AAPL'].keys())
print(stocks)
print(stocks.keys()) 
'''

def stock_performance(stocks, year='2022'):
    #Create empty dictionaries 
    performance = {}  # yearly performance of each stock 
    monthly_performance = {}  
    invested_amount = {}  
    shares_purchased = {}  

    # Store cumulative performance for each stock (this will be used for the line graph)
    cumulative_performance = {}

    # Iterate over each stock in the stocks dictionary
    for symbol in stocks:  
        money_invested = 1000
        invested_amount[symbol] = money_invested  # Store the investment amount for each stock in the dictionary 

        start_price = None

        # Initialize monthly performance for this stock symbol (months 1-12)
        monthly_performance[symbol] = [0 for _ in range(0, 12)]

        # Initialize the cumulative performance for this stock as an empty list
        cumulative_performance[symbol] = []

        previous_month_end_price = stocks[symbol][open_dates[str(int(year)-1)][-1]]['close']  # Get the first closing price of the last year

        # Iterate through each day's data for the stock
        #Enumerate is used to keep track of the index of the date in the list 
        for i,date_string in enumerate(open_dates[year]):
            month = int(date_string.split('/')[0])  # Extract the month from the date (-1 because the index starts at 0)

            # if this is not the end of the year,
            if(i != len(open_dates[year])-1):
                # if the date is not the end of the month, skip to the next date
                if(int(open_dates[year][i+1].split('/')[0]) == month):
                    continue

            data = stocks[symbol][date_string]  # Get the stock data for the date

            open_price = data['open']
            close_price = data['close']

            # keep track of the year start price
            if start_price is None:
                start_price = open_price

            # Monthly performance calculation: using the open and close prices for each month
            monthly_performance[symbol][month-1] += close_price - previous_month_end_price  # Add the difference between open and close for the month
            
            # if this is the last day of the month, calculate the monthly performance percentage
            money_invested *= (1 + (close_price / previous_month_end_price - 1))

            # Update the previous month's end price for the next iteration
            previous_month_end_price = close_price
            
            # Append the cumulative performance to the list for the stock
            cumulative_performance[symbol].append(money_invested)

        # Calculate yearly performance based on the final investment value
        performance[symbol] = ((money_invested - invested_amount[symbol]) / invested_amount[symbol]) * 100  # Percentage change from start to end

        # Store the number of shares purchased for the stock
        shares_purchased[symbol] = invested_amount[symbol] / start_price

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Print summary of performance and investments
    print(f"\nYearly and Monthly Performance for {year}:")
    for symbol in stocks:
        print(f"\nStock: {symbol}")
        
        # Print monthly performance
        print("Monthly Performance:")
        for month in range(0, 12):
            print(f"Month {months[month]}: {monthly_performance[symbol][month]:.2f}")
        
        # Print total yearly performance (percentage change)
        print(f"Total Yearly Performance: {performance[symbol]:.2f}%")
        
        # Print the number of shares purchased
        print(f"Shares Purchased with ${invested_amount[symbol]:.2f}: {shares_purchased[symbol]:.2f}")
        print("------------")

    # Plotting with Plotly for interactive graph
    
    # Create an interactive plot
    fig = go.Figure()

    # Add a line for each stock's cumulative performance
    for symbol in stocks:
        fig.add_trace(go.Scatter(
            x=months,
            y=cumulative_performance[symbol],
            mode='lines+markers',  # Plot both line and markers
            name=f"{symbol} Cumulative Performance",
            hovertemplate=f"{symbol}<br>Investment Value: $%{{y:.2f}}<br>Month: %{{x}}<extra></extra>"  # Show investment value on hover
        ))

    # Add title and labels
    fig.update_layout(
        title=f"Cumulative Stock Performance for {year}",
        xaxis_title="Months",
        yaxis_title="Investment Value ($)",
        legend_title="Stock Symbols",
        template="plotly_dark"  # Optional: Add a dark theme to the plot
    )
    
    fig.show()
    
 
stock_performance(stocks,'2022')