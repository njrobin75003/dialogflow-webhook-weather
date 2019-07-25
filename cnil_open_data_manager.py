#-------------------------------------------------------------------------------
# Name:        cnil_open_data_manager.py
# Purpose:
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
import files
importlib.reload(constants)
importlib.reload(files)

# ------------------------------------------------------------------------------------------------------------------
# Function    : get_protection_level_messages()
# Description : this function searches for a string in a specific column of dataframe.
# Returns     : a dataframe with the full file content.
# ------------------------------------------------------------------------------------------------------------------
def get_protection_level_messages (stringToLookFor, column_index, protection_level_df) :

    translation = None
    protection_level_messages = {}
    
    try:
        indexFound = False
        selectedRowIndex = -1
        returnValue = None
        cleanedStringToLookFor = stringToLookFor.lower().strip()

        for row_index, row in protection_level_df.iterrows() :
        
            stringToCollect = protection_level_df.iloc[row_index, column_index]
            cleanedStringToCollect = stringToCollect.lower().strip()

            if (cleanedStringToCollect == cleanedStringToLookFor) : 
                indexFound = True
                selectedRowIndex = row_index
                translation = protection_level_df.iloc[row_index, constants.data_protection_level_EN_col_index]
            
                protection_level_messages[constants.protection_level_messages_dictkey_1] = stringToLookFor
                protection_level_messages[constants.protection_level_messages_dictkey_2] = protection_level_df.iloc[row_index, constants.data_protection_level_EN_col_index]
                protection_level_messages[constants.protection_level_messages_dictkey_3] = protection_level_df.iloc[row_index, constants.message_col_index]
                
                if not (protection_level_df.iloc[row_index, constants.comment1_index]):
                    protection_level_messages[constants.protection_level_messages_dictkey_4] = ''
                else:
                    protection_level_messages[constants.protection_level_messages_dictkey_4] = protection_level_df.iloc[row_index, constants.comment1_index]

                if not (protection_level_df.iloc[row_index, constants.comment2_index]):
                    protection_level_messages[constants.protection_level_messages_dictkey_5] = ''
                else:
                    protection_level_messages[constants.protection_level_messages_dictkey_5] = protection_level_df.iloc[row_index, constants.comment2_index]
                
    except:
        print('An exception occurred in function get_protection_level_messages.')
        
    return protection_level_messages


def get_country_code (df, english_country_name) :
    
    try:
        country_code_and_name = df[df['Name'].str.match(english_country_name)]
        #print('Country Code and Name = \n', country_code_and_name)
        country_code = country_code_and_name.iloc[0]['Code']
        print('Country Code :', country_code, '\n')
        
    except:
        print('An exception occurred: the country "', english_country_name, '" could not be found in the file "', files.country_code_filename,'".')

    return country_code

def get_cnil_info (cnil_protection_reader, country_code) :
    
    try:        
        cnil_info = cnil_protection_reader[cnil_protection_reader['Code Pays (ISO)'].str.match(country_code, na=False)]
        #print('CNIL info = \n', cnil_info, '\n')
        
        # Just a double check to make sure we have selected the correct country.
        nom_du_pays = cnil_info.iloc[0]['Nom du Pays']
        print('Country Name (FR) :', nom_du_pays, '\n')
        
    except:
        print('An exception occurred: the country code "', country_code, '" could not be found in the file "', files.cnil_protection_filename,'".')

    return cnil_info


def get_protection_level_english_text(country_cnil_info, protection_level_messages) :
    
    protection_level_english_text = "Unknown"

    # Assumption : the cnil_info dataframe at this stage is only one row.
    # We retrieve the "Niveau de protection" reported by the CNIL from that one row.
    
    # Constants.
    protection_level_string_const = 'Niveau de protection'
    protection_level_index_const = 3
    # we assume the only possible value of rowIndex is 0 since there is only one row.
    row_index_const = 0
    
    # Get the french text from the CNIL document.
    protection_level_french_text = country_cnil_info.iloc[row_index_const, protection_level_index_const]
    print('Protection Level (FR) :', protection_level_french_text, '\n')
    
    try:
        # The protection level row which contains the 
        protection_level_messages = get_protection_level_messages(protection_level_french_text, constants.data_protection_level_FR_col_index, protection_level_messages)
        protection_level_english_text = protection_level_messages[constants.protection_level_messages_dictkey_2]
        
        print('Protection Level (EN) :', protection_level_english_text, '\n')
        
        # if necessary or for testing
        #for key, value in protection_level_messages.items() :
        #    print(key, ':', value)
        
    except:
        print('\nAn exception occurred: the corresponding English translation of "', protection_level_french_text, '" could not be found in the file "', protection_level_messages_filename, '".')

    return protection_level_english_text


def get_protection_level (english_country_name) :
    
    protection_level_english_text = "Unknown"

    print('Country Name (EN) :', english_country_name, '\n')
    
    # --- Read the 3 .csv files needed for data transfert ---
    
    try:
        # File 1 - opencnil-autorites-de-protection-vd-20190124.xlsx
        cnil_protection_reader = files.get_cnil_protection_reader()
    
        # File 2 - country-codes.xlsx
        country_codes_reader = files.get_country_codes_reader()
    
        # and get the country code from the country_name.
        # Please note the country name has to be written in English.
        country_code = get_country_code(country_codes_reader, english_country_name)
        # eventually return a list or row with return a list with the following items :
        # - Zone
        # - Code Pays (ISO)
        # - Nom du Pays
        # - Niveau de protection
        # - Membre de l'AFAPDP '\n' www.afapdp.org/pays
        # - Site internet de l'autorité indépendante
        # - Adresse postale
        # - Adresse corrigée pour les coordonnées GPS (Longitude / Latitude)
        # - Latitude
        # - Longitude
    
        # Based on the Country Code listed in the CNIL protection file, get the CNIL info provided for the country.
        country_cnil_info = get_cnil_info (cnil_protection_reader, country_code)
    
        # File 3 - protection-level-messages.csv
        protection_level_messages = files.get_protection_level_messages_reader()
        
        # Based on the CNIL info and the protection_level_messages, return the protection level in English.
        protection_level_english_text = get_protection_level_english_text(country_cnil_info, protection_level_messages)
                
    except:
        print('The country named', english_country_name, 'was not found.')
        
    return protection_level_english_text


def is_EU_country (country_list, english_country_name) :
    
    country_is_EU = False
    
    for rowIndex, row in country_list.iterrows() :
        country_name = row['EUCountry']
        if (country_name == english_country_name):
           country_is_EU = True
    
    if constants.print_logs:
        if (country_is_EU) :
            print(country_english_name, 'is in the EU.')
        else :
            print(country_english_name, 'is not in the EU.')
    
    return country_is_EU


def test_with_all_countries():
    
    country_codes_reader = get_country_codes_reader()
    #print(country_codes_reader)
    
    for rowIndex, row in country_codes_reader.iterrows() :
        country_name = row['Name']
        print('-----------------------------------------------------\n')
        get_protection_level(country_name)


def data_transfert_rule(eu_countries_reader, country_of_residence, data_destination_country) :
    
    if (is_EU_country(eu_countries_reader, country_of_residence) and (is_EU_country(eu_countries_reader, data_destination_country) == True)):
        message = 'The country of residence is {} and the data transfer destination country is {}. Both countries are in the EU. There is no issue concerning data protection, no need for an explicit clause.'.format(country_of_residence, data_destination_country)
        
    elif (is_EU_country(eu_countries_reader, country_of_residence) and (is_EU_country(eu_countries_reader, data_destination_country) == False)):
    message = 'The data protection level of {} is : {}'.format(data_destination_country, get_protection_level(data_destination_country))
    
    else :
        message = 'The country of residence is {}. This country is not in the EU. There is no issue concerning data protection, no need for an explicit clause.'.format(country_of_residence)

    return message
