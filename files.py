#-------------------------------------------------------------------------------
# Name:        files.py
# Purpose:     file with all the functions that read CSV or Excel files.
#
# Author:      Nicolas Jacques ROBIN
#
# Created:     24/07/2019
# Copyright:   (c) Servier 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pandas as pd
import importlib
import constants
importlib.reload(constants)

# ------------------------------------------------------------------------------------------------------------------
# Function    : get_cnil_protection_reader()
# Description : reads the opencnil-autorites-de-protection excel file.
# Returns     : a dataframe with the full file content.
# ------------------------------------------------------------------------------------------------------------------
def get_cnil_protection_reader () :
    
    try:
        #Get the content of the Excel file and put the entire content of the file in a reader dataframe.
        reader_dataframe = pd.read_excel(constants.cnil_protection_filename, na_filter = False)
        
        # Only for debugging
        if constants.print_header == True :
            print('-------------------------------------------------------------------------')
            print('get_cnil_protection_reader() function : first 5 rows display of the file.')
            print(reader_dataframe.head())
            print('-------------------------------------------------------------------------')

    except:
        print('An exception occurred:')
        print('The file "', constants.cnil_protection_filename, '" could not be found on the server.')
        reader_dataframe = None
        
    return reader_dataframe

# ------------------------------------------------------------------------------------------------------------------
# Function    : get_country_codes_reader()
# Description : reads a country code excel file.
# Returns     : a dataframe with the full file content.
# ------------------------------------------------------------------------------------------------------------------
def get_country_codes_reader () :
    
    try:
        #Get the content of the Excel file and put the entire content of the file in a reader dataframe.
        reader_dataframe = pd.read_excel(constants.country_code_filename, na_filter = False)

        if constants.print_header :
            print('-----------------------------------------------------------------------')
            print('get_country_codes_reader() function : first 5 rows display of the file.')
            print(reader_dataframe.head())
            print('-----------------------------------------------------------------------')
    
    except:
        print('An exception occurred:')
        print('The file "', constants.country_code_filename, '" could not be found on the server.')
        reader_dataframe = None
        
    return reader_dataframe

# ------------------------------------------------------------------------------------------------------------------
# Function    : get_protection_level_messages_reader()
# Description : reads the protection-level-messages excel file.
# Returns     : a dataframe with the full file content.
# ------------------------------------------------------------------------------------------------------------------
def get_protection_level_messages_reader () :

    try:
        #Get the content of the Excel file and put the entire content of the file in a reader dataframe.
        reader_dataframe = pd.read_excel(constants.protection_level_messages_filename)
        
        if constants.print_header :
            print('-----------------------------------------------------------------------------------')
            print('get_protection_level_messages_reader() function : first 5 rows display of the file.')
            print(reader_dataframe.head())
            print('-----------------------------------------------------------------------------------')
            
    except:
        print('An exception occurred:')
        print('The file "', constants.protection_level_messages_filename, '" could not be found on the server.')
        reader_dataframe = None

    return reader_dataframe

# ------------------------------------------------------------------------------------------------------------------
# Function    : get_eu_countries_reader()
# Description : reads the "eu-countries" excel file.
# Returns     : a dataframe with the full file content.
# ------------------------------------------------------------------------------------------------------------------
def get_eu_countries_reader () :
    
    try:
        #Get the content of the Excel file and put the entire content of the file in a reader dataframe.
        reader_dataframe = pd.read_excel(constants.eu_countries_filename)
        
        if constants.print_header :
            print('----------------------------------------------------------------------')
            print('get_eu_countries_reader() function : first 5 rows display of the file.')
            print(reader_dataframe.head())
            print('----------------------------------------------------------------------')
            
    except:
        print('An exception occurred:')
        print('The file "', constants.eu_countries_filename, '" could not be found on the server.')
        reader_dataframe = None

    return reader_dataframe
