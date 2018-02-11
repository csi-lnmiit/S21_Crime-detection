# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def file_open(string):
    
    f = open(string,"rb")
    r = csv.reader(f)
    return list(r)

###reading the data
crimes = file_open('C:\Users\Lenovo\Anaconda2\data_crimes.csv')
education = file_open('C:\Users\Lenovo\Anaconda2\data_education.csv')
poverty = file_open('C:\Users\Lenovo\Anaconda2\data_poverty.csv')

#print crimes
#print education
#print poverty

###considering columns that we require for analysis
edu_data = []
new = []
for row in education:
    for j in 3,4,16:
        new.append(row[j])  
    edu_data.append(new)
    new = []
    
#print edu_data

crime_data = []
new = []
for row in crimes:
    for j in 0,1,90:
        new.append(row[j])
    crime_data.append(new)
    new = []

#print crime_data
    
poverty_data = []
new = []
for row in poverty:
    for j in 0,3:
        new.append(row[j])
    poverty_data.append(new)
    new = []
    
#print poverty_data

###check no of districts in each table
row_count_edu = 0
row_count_crimes = 0
row_count_poverty = 0

for row in edu_data:
    row_count_edu += 1
#print row_count_edu

for row in crime_data:
    row_count_crimes += 1
#print row_count_crimes
    
for row in poverty_data:
    row_count_poverty += 1
#print row_count_poverty

###taking only districts common to both the table of datas
combined_data = [['STATE', 'DISTRICT', 'NO. OF CRIMES', 'LITERACY PERCENTAGE']]
new = []
for row_crime in crime_data:
    for row_edu in edu_data:
        if row_crime[0].upper() == row_edu[0].upper() and row_crime[1].upper() == row_edu[1].upper() and row_edu[2] != '':
            new.append(row_crime[0].upper())
            new.append(row_crime[1].upper())
            new.append(row_crime[2])
            new.append(row_edu[2])
            break
    if new != []:
        combined_data.append(new)
    new = []
    
#for j in range(0,450):
    #print combined_data[j]

row_count_data = 0

for row in combined_data:
    row_count_data += 1
#print row_count_data
            
###no of datas in which literacy percent doesnt have a valid value, ie less than or equal to 100

check =[]
for row in combined_data:
    check.append(row)
check.pop(0)

count1 = 0
for row in check:
    if float(row[3]) > 100.0:
        print "data invalid"
        count1 += 1
#print count1
        
pov =[]
for row in poverty_data:
    pov.append(row)
pov.pop(0)

###converting data to percentage and checking if data is <= 100
count2 = 0
for row in pov:
    value = float(row[1])/100.0
    if value <= 100:
        row[1] = value
    else:
        print "data invalid"
        count2 += 1
#print count2

#for j in range(0,35):
    #print pov[j]

###combining poverty data with the other data and changing to desirable data types
new_comb_data = [['STATE', 'DISTRICT', 'NO. OF CRIMES', 'LITERACY PERCENTAGE','BPL PERCENTAGE']]
new = []
row_pov_prev = "empty"
for row_pov in pov:
    for row_comb in combined_data:
        if row_pov[0].upper() == row_comb[0].upper():
            new.append(row_comb[0])
            new.append(row_comb[1])
            new.append(int(row_comb[2]))
            new.append(float(row_comb[3]))
            new.append(row_pov[1])
        if new != []:
            new_comb_data.append(new)
        new = []
            
row_count_new = 0

for row in new_comb_data:
    row_count_new += 1
#print row_count_new
    
for j in range(0,417):
    print new_comb_data[j]
    
### python always works with addresses
### .append does not allow repetition

###creating a table without the header
calc_data =[]
for row in new_comb_data:
    calc_data.append(row)
calc_data.pop(0)
    
###check if the no of crimes are whole numbers and count no of undesired values
count_3 = 0
for row in calc_data:
    if row[2] < 0 and type(row[2]) != int:
        count_3 += 1
#print count_3
    
###calculating mean number of crimes
def mean_crimes():
    sum_crimes = 0
    no_of_data = 0
    for row in calc_data:
        sum_crimes += row[2]
        no_of_data += 1
    mean = sum_crimes/float(no_of_data)
    return mean

mean_crimes = mean_crimes()
print 'Mean no of crimes in an Indian district in a certain year is '+ str(mean_crimes)

###calculating lowest and highest no of crimes and respective district and state
def highest_crimes():
    no_of_crimes = 0
    state = ''
    district = ''
    for row in calc_data:
        if row[2] > no_of_crimes:
            no_of_crimes = row[2]
            district = row[1]
            state = row[0]
    print 'The highest no of crimes committed in that year is in the district of ' + district + ' in the state of ' + state + ' and the no is ' + str(no_of_crimes)
    return no_of_crimes

highest_crimes = highest_crimes()

def lowest_crimes(x):
    no_of_crimes = x
    state = ''
    district = ''
    for row in calc_data:
        if row[2] < no_of_crimes:
            no_of_crimes = row[2]
            district = row[1]
            state = row[0]
    print 'The lowest no of crimes committed in that year is in the district of ' + district + ' in the state of ' + state + ' and the no is ' + str(no_of_crimes)
    return no_of_crimes

lowest_crimes = lowest_crimes(mean_crimes)


###calculating no of districts with crime rate above and below the mean value
def lower_than_mean(x):
    count_dist = 0
    for row in calc_data:
        if row[2] < x:
            count_dist += 1
    return count_dist

lower_than_mean = lower_than_mean(mean_crimes)
print 'No of districts with crime rate below the mean rate is ' + str(lower_than_mean)

def higher_than_mean(x):
    count_dist = 0
    for row in calc_data:
        if row[2] > x:
            count_dist += 1
    return count_dist

higher_than_mean = higher_than_mean(mean_crimes)
print 'No of districts with crime rate higher the mean rate is ' + str(higher_than_mean)

if row_count_new - 1 == lower_than_mean + higher_than_mean:
    print 'Total no of districs considered in analysis is ' + str(lower_than_mean + higher_than_mean)
###256 + 160 = 416. no missing data
    
###finding mean literacy and BPL percent
def mean_literacy():
    sum_lit = 0
    no_of_data = 0
    for row in calc_data:
        sum_lit += row[3]
        no_of_data += 1
    mean = sum_lit/float(no_of_data)
    return mean

mean_literacy = mean_literacy()
print 'Mean literacy rate in an Indian district in a certain year is '+ str(mean_literacy) + '%'

def mean_BPL():
    sum_BPL = 0
    no_of_data = 0
    for row in calc_data:
        sum_BPL += row[4]
        no_of_data += 1
    mean = sum_BPL/float(no_of_data)
    return mean

mean_BPL = mean_BPL()
print 'Mean BPL percent population in an Indian district in a certain year is '+ str(mean_BPL) + '%'

###no of districts below and above mean literacy %
def lit_lower_than_mean(x):
    count_dist = 0
    for row in calc_data:
        if row[3] < x:
            count_dist += 1
    return count_dist

lit_lower_than_mean = lit_lower_than_mean(mean_literacy)
print 'No of districts with literacy rate below the mean rate is ' + str(lit_lower_than_mean)

def lit_higher_than_mean(x):
    count_dist = 0
    for row in calc_data:
        if row[3] > x:
            count_dist += 1
    return count_dist

lit_higher_than_mean = lit_higher_than_mean(mean_literacy)
print 'No of districts with literacy rate higher the mean rate is ' + str(lit_higher_than_mean)

if row_count_new - 1 != lit_lower_than_mean + lit_higher_than_mean:
    print 'data missing'
    
###no of districts below and above mean BPL %
def bpl_lower_than_mean(x):
    count_dist = 0
    for row in calc_data:
        if row[4] < x:
            count_dist += 1
    return count_dist

bpl_lower_than_mean = bpl_lower_than_mean(mean_BPL)
print 'No of districts with BPL % below the mean % is ' + str(bpl_lower_than_mean)

def bpl_higher_than_mean(x):
    count_dist = 0
    for row in calc_data:
        if row[4] > x:
            count_dist += 1
    return count_dist

bpl_higher_than_mean = bpl_higher_than_mean(mean_BPL)
print 'No of districts with BPL % higher the mean rate is ' + str(bpl_higher_than_mean)

if row_count_new - 1 != bpl_lower_than_mean + bpl_higher_than_mean:
    print 'data missing'
    
###highest and lowest literacy and BPL %
def highest_literacy():
    lit_percent = 0
    state = ''
    district = ''
    for row in calc_data:
        if row[3] > lit_percent:
            lit_percent = row[3]
            district = row[1]
            state = row[0]
    print 'The highest literacy percentage in that year is in the district of ' + district + ' in the state of ' + state + ' and the no is ' + str(lit_percent)
    return lit_percent

highest_literacy = highest_literacy()

def lowest_literacy(x):
    lit_percent = 0
    state = ''
    district = ''
    for row in calc_data:
        if row[3] < x:
            lit_percent = row[3]
            district = row[1]
            state = row[0]
    print 'The lowest literacy percentage in that year is in the district of ' + district + ' in the state of ' + state + ' and the no is ' + str(lit_percent)
    return lit_percent

lowest_literacy = lowest_literacy(mean_literacy)

def highest_bpl_percent():
    bpl_percent = 0
    state = ''
    district = ''
    for row in calc_data:
        if row[4] > bpl_percent:
            bpl_percent = row[4]
            district = row[1]
            state = row[0]
    print 'The highest bpl percentage in that year is in the district of ' + district + ' in the state of ' + state + ' and the no is ' + str(bpl_percent)
    return bpl_percent

highest_bpl_percent = highest_bpl_percent()

def lowest_bpl_percent(x):
    bpl_percent = 0
    state = ''
    district = ''
    for row in calc_data:
        if row[4] < x:
            bpl_percent = row[4]
            district = row[1]
            state = row[0]
    print 'The lowest bpl percentage in that year is in the district of ' + district + ' in the state of ' + state + ' and the no is ' + str(bpl_percent)
    return bpl_percent

lowest_bpl_percent = lowest_bpl_percent(mean_BPL)

crime = []
lit = []
bpl = []
for row in  calc_data:
    crime.append(row[2])
for row in  calc_data:
    lit.append(row[3])
for row in  calc_data:
    bpl.append(row[4])
    
plt.bar(lit,crime)
plt.show()
plt.bar(bpl,crime)
plt.show()
plt.scatter(bpl,lit)
plt.show()
plt.scatter(lit,bpl)
plt.show()
plt.hist(crime, bins = 20)
plt.show()
plt.hist(lit, bins = 20)
plt.show()
plt.hist(bpl, bins = 20)
plt.show()


