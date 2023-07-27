import pandas as pd
import yfinance as yf
import argparse
from stocksymbol import StockSymbol
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
import sys
import os
# api_key is mine here 
# Use yours by filling this form of stocksymbol api
#
application_path = os.path.dirname(sys.executable)
api_key = 'daf2adb4-22db-4ded-becd-b7c7aeddc75a'
ss = StockSymbol(api_key)


# The function works to get all the stocks available in us and india
def get_total_ss(ss):
    symbol_list_us = ss.get_symbol_list(market="US")
    symbol_stock_us = []
    for i in range(0,len(symbol_list_us)):
        a = symbol_list_us[i]['symbol']
        symbol_stock_us.append(a)
    symbol_list_india = ss.get_symbol_list(market="india")
    symbol_stock_india = []
    for i in range(0,len(symbol_list_india)):
        a = symbol_list_india[i]['symbol']
        symbol_stock_india.append(a)
    
    total_ss= symbol_stock_india + symbol_stock_us
    total_ss.sort()
    return list(total_ss)

total_ss = get_total_ss(ss)

# len of the list containing the all the similar stock
def search_len(list_ss,search_key):
    search_key = search_key.upper()
    t = []
    for i in list_ss:
        if i.startswith(search_key):
            t.append(i)
    return len(t)

# Search for all the stocks starting wirh search_key. If nothing like that exists, it return No such stock present.
# Else shows the list of top 10 matching stocks
def search(list_ss,search_key):
    search_key = search_key.upper()
    t = []
    for i in list_ss:
        if i.startswith(search_key):
            t.append(i)
    if len(t) == 0:
        print("No such stock present in the US and Indian Marketplace")
    else:
        print("There are {0} stocks starting with {1}. The top 10 of which are : ".format(search_len(list_ss,search_key),search_key))
        for j in t[:10]:
            print(j)

# Used to search when view stock name is incomplete in view command
def search_view(list_ss,search_key):
    search_key = search_key.upper()
    t = []
    for i in list_ss:
        if i.startswith(search_key):
            t.append(i)
    if len(t) == 0:
        print("No such stock present in the US and Indian Marketplace")
    else:
        print("Maybe you mean one of these stocks symbols : ")
        for j in t[:20]:
            print(j)
            
# shows data of stock over x days
def stock_x_days(list_ss, stock, x=10):
    if stock not in list_ss:
        print("No such stock available")
    else:
        if x >= 60:
            x = 60
        xdays = str(x) + 'd'
        stock_var = yf.Ticker(stock)
        stock_hist = stock_var.history(period=xdays)
        stock_data = pd.DataFrame(stock_hist)
        stock_data = stock_data.reset_index()
        stock_data['Date'] = pd.to_datetime(stock_data['Date']).dt.date
        return stock_data

# prints stock data
def print_stock(data):
    data = data[['Date','Open','High','Low','Close']]
    print(data)

#Used to predict the stock value for next 5 days
def real_production(train_data,model_name,start,end,start2):
    if model_name == 'model_lr':
        X = train_data[start].values.reshape(-1, 1)
        y = train_data[end].values
        model_lr = LinearRegression()
        model_lr.fit(X, y)
        
        train_data2 = train_data.copy()
        train_data2[start2] = train_data2[start].shift(-1)
        train_data2.drop(columns=start)
        train_data2.dropna(inplace=True)
        X2 = train_data2[end].values.reshape(-1,1)
        y2 = train_data2[start2].values
        model_lr2 = LinearRegression()
        model_lr2.fit(X2,y2)
        tclose = y[-1]
        l = []
        l2 = []
        for i in range(0,5):
            predicted_c_o = model_lr2.predict([[tclose]])
            l.append(round(predicted_c_o[0],2))
            predict_o_c = model_lr2.predict([[l[-1]]])
            l2.append(round(predict_o_c[0],2))
            tclose = l2[-1]
        print_df = pd.DataFrame({'Open':l,'Close':l2})
        print(print_df)

# can shows stock_data for more than 60 days       
def stock_x_days_unlimited(list_ss, stock, x=10):
    if stock not in list_ss:
        print("No such stock available")
    else:
        xdays = str(x) + 'd'
        stock_var = yf.Ticker(stock)
        stock_hist = stock_var.history(period=xdays)
        stock_data = pd.DataFrame(stock_hist)
        stock_data = stock_data.reset_index()
        stock_data['Date'] = pd.to_datetime(stock_data['Date']).dt.date
        return stock_data

# made so that continuous inputs can be supported and no need to write the same command again in cli
def continouous_inputs():
    while True:
        user_input = input("Enter a valid command or 'help' for more info \n or 'exit' to quit the program.    ").split(' ')
        if user_input[0].lower() == 'exit':
            break
        
        try:
            if user_input[0] == 'help':
                print()
                print("#######################################")
                print("Use the following commands to do the following : ")
                print("Use the command with appropriate syntax else it will not function and show error.")
                print("DO NOT USE <> shown in syntax")
                print("help - get all the information about the necessary functions")
                print("Syntax : help")
                print("search - search a particular stock symbol")
                print("Syntax : search <stock_name>")
                print('view - view the stock prices between last 2 months to 10 days')
                print("Syntax : view <stock_name> <number_of_days>")
                print("predict - predict the value of the stock for next 5 days")
                print("Syntax : predict <stock_name>")
                print("#######################################")
                print()
            elif user_input[0] == 'search':
                print()
                print("#######################################")
                search(total_ss,user_input[1])
                print("#######################################")
                print()
            elif user_input[0] == 'view':
                print()
                print("#######################################")
                if user_input[0] == 'view':
                    stock = user_input[1].upper()
                    days = int(user_input[2])
                    if stock not in total_ss:
                        search_view(total_ss, stock)
                    else:
                        data = stock_x_days(total_ss, stock, days)
                        print_stock(data)
                print("#######################################")
                print()
            elif user_input[0] == 'predict':
                print()
                print("#######################################")
                stock = user_input[1].upper()
                if stock not in total_ss:
                    search_view(total_ss,stock)
                else:
                    data = stock_x_days_unlimited(total_ss, stock, 120)
                    real_production(data,'model_lr','Open','Close','Open2')
                print("#######################################")
                print()
            else:
                print()
                print("#######################################")
                print("Syntax Error, use help to know proper syntax .\nEnter a valid command.")
                print("#######################################")
                print()
        except:
            print("Invalid input.")
            print("Enter a valid command or 'help' for more info \n or 'exit' to quit the program    ")
            
def main():
    parser = argparse.ArgumentParser(description="The stock prediction CLI ")
    args = parser.parse_args()

    continouous_inputs()

if __name__ == "__main__":
    main()
    input()