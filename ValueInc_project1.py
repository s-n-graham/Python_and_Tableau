#This link is for the Tableau dashboard
#https://public.tableau.com/authoring/ValueInc_Dashboard1stPyProject/Dashboard1#1

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 15:55:19 2022

@author: simpp
"""

import pandas as pd

# file_name = pd.read_csv('file.csv')

data = pd.read_csv('transaction.csv')

data = pd.read_csv('transaction.csv', sep=';')

#summary of data
data.info()

CostPerItem = 11.73
SellingPricePerItem = 21.11
NumberOfItemsPurchased = 6

###############################################################
#CostPerTransaction Column
#CostPerTransaction = CostPerItem * NumberOfItemsPurchased
CostPerItem = data['CostPerItem']
NumberOfItemsPurchased = data['NumberOfItemsPurchased']
CostPerTransaction = CostPerItem*NumberOfItemsPurchased
data['CostPerTransaction'] = CostPerTransaction

#################################################################
#SalesPerTransaction Column
data['SalesPerTransaction'] = data['SellingPricePerItem']*data['NumberOfItemsPurchased']

################################################################
#Profit = Sales - Cost
data['ProfitPerTransaction'] = data['SalesPerTransaction']-data['CostPerTransaction']

################################################################
#Markup = (Sales - Cost) / Cost
data['Markup'] = (data['SalesPerTransaction']-data['CostPerTransaction']) / data['CostPerTransaction']
#or
data['Markup'] = data['ProfitPerTransaction'] / data['CostPerTransaction']
rounded = round(data['Markup'],2)
data['Markup'] = rounded

################################################################
#Combining fields (both integer and strings)
date = data['Day'].astype(str)+'-'+data['Month']+'-'+data['Year'].astype(str)
data['Date'] = date

################################################################
#use iloc to view specific columns and rows
data.iloc[0] #1st row index 0
data.iloc[0:3] #1st 3 rows from 0
data.iloc[-1:] #last row
data.iloc[:,4] #all rows on column 4
data.iloc[1,2] #1st row, 2nd column(excluding 0)
#even better
data.head(5) #brings 1st 5 rows from 0

#################################################################
#Cleaning
#Using Split
#new_var = column.str.split('sep' , expand = True)
split_col = data['ClientKeywords'].str.split(',' , expand=True)

#create new columns from split data
data['ClientAge'] = split_col[0]
data['ClientType'] = split_col[1]
data['LengthOfContract'] = split_col[2]

#replace function
data['ClientAge'] = data['ClientAge'].str.replace('[', '')
data['LengthOfContract'] = data['LengthOfContract'].str.replace(']', '')

#lowerCase
data['ItemDescription'] = data['ItemDescription'].str.lower()

#################################################################
#Merge different files, join datasets
seasons = pd.read_csv('value_inc_seasons.csv', sep=';')

data = pd.merge(data, seasons, on = 'Month') #join on matching key, 'month'

#drop a column (axis 1 is a colum, 0 is a row)
data = data.drop('ClientKeywords', axis = 1)
data = data.drop(['Month','Year'], axis = 1) #I already dropped 'Day'

#Export to CSV
data.to_csv('ValueInc_Clean.csv', index = False)
