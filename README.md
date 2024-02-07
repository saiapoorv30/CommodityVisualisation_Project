# CommodityVisualisation_Project
This program will filter the data for each record from the produce_csv.csv and represent the data in the grouped bar charts.
We are importing the modules into the program
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
