#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 09:05:54 2022

Main:
    creates file pointer
    initializes country and regime lists based off filepointer
    prints regime options (menu)
    prompts user for option
    while option is not quit:
        if option 1:
            Prompts for a country
            Error checks to ensure country in country list
            finds regime of country using history of country function and prints according to first letter of regime(an or a)
        elif option 2:
            prompts for a regime, error checks to ensure in regime list
            finds allies using historical allies function and seprates them by commas, stripping last comma
            prints regime of countries and formatted countries
        elif option 3:
            prompts for how many countries to display, error checks to ensure a positive int
            finds list of top countries using top coup function, prints it in according format
        else:(invalid)
            prints error statement, reprompts for option
    prints closing statement(the end)
            
            
            
    
"""
#import statements
import csv
from operator import itemgetter
#initializes variables
REGIME=["Closed autocracy","Electoral autocracy","Electoral democracy","Liberal democracy"]
MENU='''\nRegime Options:
            (1) Display regime history
            (2) Display allies
            (3) Display chaotic regimes        
    '''

def open_file():
    '''
    prompts for a file name until file can be opened
    returns file pointer
    '''
    i = 0#initializes variable to exit while loop
    while i ==0:
        try: 
            file_name = input("Enter a file: ")#prompts for file name
            fp = open(file_name,'r')# tries to open file
            return fp #returns filepointer if file can be opened
        except FileNotFoundError:#except for if file cannot be opened
            print("File not found. Please try again.")#error statement
            
         
def read_file(fp):
    ''' 
    reads through file referencing file pointer
    goes through file and creates a list of countries and list of regimes(list of lists) that corresponds with country list
    returns two lists(country list and regime lsit)
    
    '''
    reader = csv.reader(fp)#sets reader to csv of filepointer
    next(reader,None)#skips first line
    #initalizes variables
    country_names = []
    list_of_regime_lists = []
    for line in reader: #reads through each list(line) in file
        #if country isn't in country list, adds country to country list and adds regime value as a list to regime list
        if line[1] not in country_names:
            country_names.append(line[1])
            list_of_regime_lists.append([int(line[4])])
        #else if country is in list, appends regime to the list in the list that corresponds to country
        elif line[1] in country_names:
            index = country_names.index(line[1])
            list_of_regime_lists[index].append(int(line[4]))
    return country_names,list_of_regime_lists #returns country list and regime list
   
    
def history_of_country(country,country_names,list_of_regime_lists):
    ''' 
    finds the regime of a country based off of their history
    returns the regime as a string
    '''
    index = country_names.index(country)#sets the index of the country in country names as a variable
    list_count = []#initializes list
    for i in range(0,4):#for loop that goes from 0-3(corresponds with regime)
        list_count.append(list_of_regime_lists[index].count(i))#appends the number of regimes in order from 0-3
    max_val = list_count.index(max(list_count))#finds the index of the max value of the regimes
    return REGIME[max_val]#returns the string of the regime by referencing the REGIME list
    

def historical_allies(regime,country_names,list_of_regime_lists):
    ''' 
    finds the countries that have the same regime historically(allies)
    returns allies list alphabetically
    '''
    country_list=[]#initializes country list
    for country in country_names:#goes through each country
        if regime == history_of_country(country,country_names,list_of_regime_lists):#if the country's regime is the parameter regime
            country_list.append(country)#appends country to country list
    return sorted(country_list)#returns sorted country list

def top_coup_detat_count(top, country_names,list_of_regime_lists):          
    ''' 
    finds the top countries with highest coups
    returns list of top coup countries
    '''
    coup_list = []#initializes list
    for country in country_names:#goes through each country
        coup = 0#sets voup value to 0
        for i in range(1,len(list_of_regime_lists[country_names.index(country)])):#goes through each value in list of lists of regimes
            if list_of_regime_lists[country_names.index(country)][i] != list_of_regime_lists[country_names.index(country)][i-1]:#if current value is not equal to last value,
                coup+=1#adds 1 to coup value 
        coup_list.append((country,coup))#appends tuple with country and amount of coups
    coup_list.sort(key=itemgetter(1),reverse=True)#sorts list of tups by coups in descending order
    new_list = coup_list[0:top]#Creates a new list that has the top countries and their coups
    return new_list #returns list
    
def main():
    # by convention "main" doesn't need a docstring
    fp = open_file()#sets file pointer using open file function
    country_names,list_of_regime_lists = read_file(fp)#sets country list and regime list using read file function
    print(MENU)#prints options
    option = input("Input an option (Q to quit): ")#prompts for option
    #while loop that runs until user wants to quit
    while option != 'Q' and option !='q':
        #if user inputs 1
        if option == '1':
           country = input( "Enter a country: ")#prompts for a country
           while country not in country_names:#error checks for if country is in country list
               print("Invalid country. Please try again.")#error statement
               country = input( "Enter a country: ")#reprompts for country
           regime = history_of_country(country, country_names, list_of_regime_lists)#sets regime using history of country function
           if regime == REGIME[0] or regime == REGIME[3]:#non vowel starting regimes
               print("\nHistorically {} has mostly been a {}".format(country,regime))#prints country and regime
           elif regime == REGIME[1] or regime == REGIME[2]:#vowel starting regimes
               print("\nHistorically {} has mostly been an {}".format(country,regime))#prints country and regime
        #if user inputs 2
        elif option =='2':
            regime_2 = input("Enter a regime: ")#prompts for regime
            while regime_2 not in REGIME:#error checks for if regime in regime list
                print("Invalid regime. Please try again.")#error statement
                regime_2 = input("Enter a regime: ")#reprompts for regime
            allies = historical_allies(regime_2, country_names, list_of_regime_lists)#sets allies using historical allies function
            string_allies = ''#initializes string of allies
            for ally in allies:#goes through each ally in list
                string_allies += ally + ', '#adds ally to string with a , 
            print("\nHistorically these countries are allies of type:",regime_2)#prints regime
            print(string_allies.strip(', '))#prints stripped ally string
        #if user inputs 3
        elif option == '3':
           top = input("Enter how many to display: ")#prompts for top number
           a =1#sets variable to 1 to exit while loop
           while a ==1:#while variable is unchanged
               try:
                   int(top)#tries to set top to an int
                   a =0#exits while loop
               except ValueError:#if unable to change to int
                   print("Invalid number. Please try again.")#error statement
                   top = input("Enter how many to display: ")#reprompt for top
           coup_list = top_coup_detat_count(int(top), country_names, list_of_regime_lists)#sets top coups list by using top coup function
           print("\n{: >25} {: >8}\n".format('Country','Changes'))#prints header
           for i in coup_list:#goes through each tuple in list
               print("{: >25} {: >8}".format(i[0],i[1]))#prints country and number of coups for each country
        #if user doesn't input 1,2,3 or q/Q
        else:
            print("Invalid choice. Please try again.")#error statement
            option = input("Input an option (Q to quit): ")#reprompts for option
        
        print(MENU)#prints options
        option = input("Input an option (Q to quit): ")#reprompts for option
        
    print("The end.")#closing statement

# These two lines allow this program to be imported into other code
# such as our function_test code allowing other functions to be run
# and tested without 'main' running.  However, when this program is
# run alone, 'main' will execute.  
if __name__ == "__main__": 
    main() 