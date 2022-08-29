# -*- coding: utf-8 -*-

#Tableau link:
#https://public.tableau.com/app/profile/simon.graham1440/viz/BlueBank_16617874973130/BlueBankLoans?publish=yes

"""
Created on Tue Aug 16 12:32:42 2022

@author: simpp
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

with open('loan_data_json.json') as json_file:
    data = json.load(json_file)

#transform raw data to dataframe
loanData = pd.DataFrame(data)

#find unique values, ordered from a column
loanData['purpose'].unique()

#describe data
loanData.describe()
#describe for specific column
loanData['int.rate'].describe()
loanData['fico'].describe()
loanData['dti'].describe() #debt to income ratio -0 is good +0 not good

#using numpy for exp() exponent f to get annual income
income = np.exp(loanData['log.annual.inc'])
loanData['annualIncome'] = income

#Fico score
#for the 1st 10 of index

length = len(loanData)
ficoCat = []
for x in range(0,length):
    category = loanData['fico'][x]
    
    try:
        if category >= 300 and category < 400:
            cat = 'Very poor'
        elif category >= 400 and category < 600:
            cat = 'Poor'
        elif category >= 601 and category < 660:
            cat = 'Fair'
        elif category >= 660 and category < 700:
            cat = 'Good'
        elif category >= 700:
            cat = 'Excellent'
        else:
            cat = 'Error: Out of range or NULL'
    except:
        cat = 'Unknown'
            
    ficoCat.append(cat)

ficoCat = pd.Series(ficoCat)
loanData['fico.category'] = ficoCat   

#create column with certain condition (pandas)
#if interest rate > 0.12 is high, else low

loanData.loc[loanData['int.rate']>0.12,'int.rate.type'] = 'High'
loanData.loc[loanData['int.rate']<=0.12,'int.rate.type'] = 'Low'

#find number of loans per loan category, to plot them
catPlot = loanData.groupby(['fico.category']).size()
catPlot.plot.bar(color = 'green', width=0.8)
plt.show()

purposeCount = loanData.groupby(['purpose']).size()
purposeCount.plot.bar(color = 'red', width=0.4)
plt.show()

#make scatter plots. higher the income = less debt
ypoint = loanData['annualIncome']
xpoint = loanData['dti']
plt.scatter(xpoint, ypoint)
plt.show()

loanData.to_csv('loan_cleaned.csv', index = True)
