'''
Program: Commodity Data Visualization
Author: Sai Apoorv Makthala
Description: This program will filter the data for each record from the produce_csv.csv and represent the data in the grouped bar charts.
Revisions:
                00: We are importing the modules into the program
                01: We are creating a function that accepts a list as one input and one argument for character padding to print indexes. This can be accomplished by allocating wid+enum+2 (72) characters for the index and text and setting aside 20 characters for the text itself.
                02: Announce and prompt the input to the user.
                03: We are reading the data from the csv file using the csv.reader() function and organize the data in the format: Commodity, Date, Location, Price
		04: We are filtering the unique commodities, dates and locations and storing them in a set.
		05: We are calling the function to print each unique commodity with index in three coloumns and ask user for commodity.
		06: Announce and prompt the available cities to the user.
		07: We are filtering the data based on commodity, dates range and location
		08: We are calculating the average price of commodity in each city based on commodities and cities.
		09: We are creating unique commodity vs. average price bar graphs for each city, then aggregating the graph for analysis and visualizing the data.
'''
#Import the modules into the program
import csv
from datetime import datetime
import plotly.offline as py
import plotly.graph_objs as go


#In order to display data across three columns, create a function that accepts a list as one input and one argument for character padding to print indexes. This can be accomplished by allocating wid+enum+2 (72) characters for the index and text and setting aside 20 characters for the text itself.
def columnPrint(x,enum=0, wid = 20):
    s = ''
    for n,item in enumerate(x):
        if len(s) < 3 * (wid+enum+2):
            if enum:
                s = s + f'[{n:{enum}}]'
            s = s + f'{item:<20}'
        else:
            print(s)
            s = ''
            if enum:
                s = s + f'[{n:{enum}}]'
            s = s + f'{item:<20}'
    if s:
        print(s)

        
#Announce and prompt the input to the user
print(f'\n{"="*30}\n{"Analysis of commodity data":^30}\n{"="*30}\n')

#Read the data from the csv file using the csv.reader() function and organize the data in the format: Commodity, Date, Location, Price
data = []
csvfile = open('produce_csv.csv','r')
reader = csv.reader(csvfile)
for row in reader:
    if reader.line_num == 1:
        data_locations = row[2:]
    else:
        for location, value in zip(data_locations, row[2:]):
            row_num = len(data)
            data.append(row[:2])
            data[row_num].append(location)
            data[row_num].append(float(value.replace('$','')))
            date = datetime.strptime(data[row_num][1],'%m/%d/%Y')
            data[row_num][1] = date;
csvfile.close()

#Filtering the unique commodities, dates and locations and storing them in a set. 
data_commodity = list(sorted(set([x[0] for x in data])))
data_dates = list(set([x[1] for x in data]))
data_locations = list(sorted(set([x[2] for x in data])))

#Calling the function to print each unique commodity with index in three coloumns and ask user for commodity.
print(f'\n Select Products by Number...\n')
columnPrint(data_commodity,2)
req_commodity = [int(i) for i in (input("Enter product numbers separated by spaces: ")).split()]
selected_commodity = [comm for i, comm in enumerate(data_commodity) for j in req_commodity if int(j) == i]
print(f'\nSelected Products: {", ".join(selected_commodity)}')

#Calling the function to print dates with index in 3 coloumns and print the earliest and the latest date and take the index from the user. 
print(f'\nSelect Date by Number....\n')
data_dates.sort()
formatted_new_dates = [datetime.strftime(date,"%Y-%m-%d") for date in data_dates]
columnPrint( formatted_new_dates,2)
print(f'\nThe Earliest Available Date is: {min(formatted_new_dates)}')
print(f'\nThe Latest Available Date is: {max(formatted_new_dates)}')
user_req_dates = [int(i) for i in (input(f'Enter start/end date numbers separated by a space: ')).split()]
date_range_select = [d for i,d in enumerate(formatted_new_dates) if int(min(user_req_dates)) <= i <= int(max(user_req_dates))]
print(f'Dates from  {min(date_range_select)} to {max(date_range_select)}')

#Announce and prompt the available cities to the user.
print('\nSelect Locations by Number...\n')
for i,city in enumerate(data_locations):
    print(f'<{i}> {city}')
    user_req_loc = [int(i) for i in (input(f'Enter location numbers separated by spaces: ')).split()]
    location_select = [loc for index_loc in user_req_loc for ind, loc in enumerate(data_locations) if int(index_loc) == ind ]
    print(f'Selected Locations: {" ".join(location_select)}')

#Filtering the data based on commodity, dates range and location.   
data_new = list(filter(lambda row:row[0] in selected_commodity and (data_dates[int(user_req_dates[0])] <= row[1] <= data_dates[int(user_req_dates[1])]) and row[2] in location_select,data))

#Calculating the average price of commodity in each city based on commodities and cities.
city_prices = []
commodity_miss = set()
for x in location_select:
    price_by_city = []
    for y in selected_commodity:
        filteredData = (list(filter(lambda a: a[2] in x and a[0] in y, data_new)))
        avg_commodity_price = [i[3] for i in filteredData]
        if len(avg_commodity_price) > 0:
            price_by_city.append(round(sum(avg_commodity_price)/len(avg_commodity_price),2))
        else:
            commodity_miss.add(y)
    city_prices.append(price_by_city)
for i in commodity_miss:
    selected_commodity.pop(selected_commodity.index(i))

#Creating unique commodity vs. average price bar graphs for each city, then aggregating the graph for analysis and visualizing the data.
data_final = [go.Bar(x=selected_commodity,
                         y = list(city_prices[i]),
                         name = j) for i, j in enumerate(location_select)]
fig_graph = go.Figure(data = data_final,
                layout = go.Layout(barmode='group'))
fig_graph.update_layout(
yaxis = dict(title = 'Average Price',fixedrange = True, tickprefix = '$', tickformat = ',.2f',showgrid = True),
xaxis = dict(title = 'Product'),
title = (f' Produce Prices from {min(date_range_select)} to {max(date_range_select)}.'+(f'Produce {", ".join(commodity_miss)} prices not found for given date range' if commodity_miss else '')),
legend = dict(title = "Cities" ),
plot_bgcolor = "silver",
paper_bgcolor = "white",
showlegend = True
)

py.plot(fig_graph,filename = 'CommodityDataVisualization.html')

print(f'{len(data_new)} records have been selected.')
