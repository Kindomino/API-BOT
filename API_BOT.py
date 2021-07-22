from pip._vendor import requests
from datetime import datetime
from datetime import date
import pprint
import time
import json

#***FUNCTIONS***
# Python code to convert string to list
def convert(string):
    li = list(string.split(" "))
    return li
# Python code to convert backup group path to list
def convert2(string):
    li = list(string.split("\\"))
    return li





#**************************************************************************************************
# Change the credentials in s.auth to your own redstor login ('user', 'password') to work with
# your own redstor enviroment   
#**************************************************************************************************
#***REDSTOR API REQUEST FOR ALL REDSTOR ACCOUNTS***
#  Set your login details ! Defaulting on prov portal login
s = requests.Session()
#s.auth = ('shreports', 'KickingMemory2021')
s.auth = ('sean.swanepoel', '$wanep03!')





#**************************************************************************************************
# if list_BackupGroup[counter_BackupGroup] == 'Agency Partners' and check_AgencyPartner == False:  
# at the line above you can manipulate 'Agency Partners' to change what group you wish to filter by 
# entire path is scanned so any part of the path EXCEPT ACCOUNT NAME can be filtered                
#**************************************************************************************************
print ("***FILTERING REDSTOR ACCOUNTS***")
request_Accounts = s.get('https://api.pro.redstor.com/api/odata/Accounts').json()['value']
param_request_Accounts_Skip = 0 # parameter to skip through pages of redstor accounts in API request
counter_AccountsScanned = 0 # counter for total accounts scanned
counter_request_Accounts = 0 # counter to iterate through each redstor account's information
filtered_request_Accounts = [] # list which will be filled with filtered redstor accounts
while len(request_Accounts) == 1000: # while counter is less than length of list of redstor accounts
    request_Accounts = s.get(f'https://api.pro.redstor.com/api/odata/Accounts?$skip={param_request_Accounts_Skip}').json()['value'] # API request for Redstor accounts
    time.sleep(1)
    counter_AccountsAdded = 0 # counter for total accounts added
    while counter_request_Accounts < (len(request_Accounts)): # while counter is less than length of list of Resdstor accounts
        list_BackupGroup = convert2(request_Accounts[counter_request_Accounts]['BackupGroup']) # create temporary list to place the seperated path of redstor account into
        length_list_BackupGroup = len(list_BackupGroup) # length of list_BackupGroup to help iterate through the contents later 
        counter_BackupGroup = 0 # counter to iterate through list_BackupGroup's cells for checks
        check_AgencyPartner = False # check for an agency partner account
        while counter_BackupGroup < length_list_BackupGroup: # while counter is less than length of list_BackupGroup
            if list_BackupGroup[counter_BackupGroup] == 'Agency Partners' and check_AgencyPartner == False: # LINE OF CODE WITHIN DOCUMENTATION ABOVE, checks if within path 'Agency Partners' is found
                check_AgencyPartner = True # classify redstor account in question as an agency partner
            counter_BackupGroup += 1 #iterate to scan next cell in list of backupgroup path
            
        if check_AgencyPartner == True and request_Accounts[counter_request_Accounts]['Active'] == True and request_Accounts[counter_request_Accounts]['LastBackupDate'] is not None: # if redstor account in question is an agency partner and classified as active
            dict_RedstorAccount = request_Accounts[counter_request_Accounts] # grab dictionary containing redstor account's info and put into a new dictionary 
            dict_copy = dict_RedstorAccount.copy() # create a copy of dictRedstorAccount
            filtered_request_Accounts.append(dict_copy) # add the copy of dictRedstorAccount to the list of filtered redstor accounts
            counter_AccountsAdded += 1 # iterate to count total accounts added
        
        counter_request_Accounts += 1 # iterate to scan next cell in list of redstor accounts
        counter_AccountsScanned += 1 # iterate to count total accounts scanned
    
    counter_request_Accounts = 0 
    param_request_Accounts_Skip += 1000 # iterate to API request next 1000 redstor accounts 
    print ("REDSTOR ACCOUNTS SCANNED: ", counter_AccountsScanned)
    print ("REDSTOR ACCOUNTS ADDED: ", counter_AccountsAdded)
print("TOTAL ACCOUNTS ADDED: ", len(filtered_request_Accounts))





#**************************************************************************************************
# to manipulate token_refresh for your own zohodesk enviroment setup a refresh token beforehand on 
# postman and grab orgID within variable 'headers' by heading onto your zohodesk enviroment and
# select the settings tab on the top right, select 'API' under 'DEVELOPER SPACE' and orgId will be
# found at the bottom of the page                 
#**************************************************************************************************
#***ZOHO DESK API REQUEST FOR TICKETS***
# Grabbing required information for listing tickets and storing them in a variable
#ZOHODESK FOR PROTOS ENVIROMENT
#token_Refresh = "1000.fa7c3477d27a33d4e9df3441236aaf1e.24367a4034451565c64eecc13eda4d75"
#client_Id = "1000.C800QHYEAC2X5ONRKWESJMLL1S6V3F"
#client_Secret = "e5a46872f4e7f126e2f066a4ec30c54be6efc6c1c4"
#request_RefreshToken = requests.post(f'https://accounts.zoho.com/oauth/v2/token?refresh_token={token_Refresh}&client_id={client_Id}&client_secret={client_Secret}&grant_type=refresh_token').json()
#token_Access = str(request_RefreshToken['access_token'])
#headers = {'orgId': ('732503526') , 'Authorization': f'Zoho-oauthtoken {token_Access}'}

#ZOHODESK FOR PERSONAL ENVIROMENT
token_Refresh = "1000.9ee7878e462dce91ba93370cc8ae4c89.00605d5a1acbe96c72f5cebc59d385ab" # refresh token used to fetch new access token for access to zohodesk API requests, lasts forever
client_Id = "1000.YDOPB4JT48NG4LP3V9VPKFINZIECIR" # client id used to link API request to your zohodesk enviroment
client_Secret = "1498df3bd8ab23e6d9e4b7fe742c6e7e663de67919" # client secret used to link API request to your zohodesk enviroment
request_RefreshToken = requests.post(f'https://accounts.zoho.com/oauth/v2/token?refresh_token={token_Refresh}&client_id={client_Id}&client_secret={client_Secret}&grant_type=refresh_token').json() # API request for access token
token_Access = str(request_RefreshToken['access_token']) # grabbing just the access token from API request
headers = {'orgId': ('751922355') , 'Authorization': f'Zoho-oauthtoken {token_Access}'} # headers for any further Zohodesk API requests 





#**************************************************************************************************
# Nothing will need to be changed in this section 
#**************************************************************************************************
print(" \n \n " + "***GRABBING ALL TICKETS AND PLACING THEM IN LIST***")
param_from = 0 # from parameter in request_ListTickets API request
list_AllTickets = [] # list which will hold all Zohodesk tickets 
check_ListIsDone = False # boolean for whether all tickets have been grabbed or not
while check_ListIsDone == False:
    try:
        request_ListTickets = requests.get(f"https://desk.zoho.com/api/v1/tickets?from={param_from}&limit=99", headers = headers).json() # API request for next 99 tickets
        time.sleep(1)

    except json.decoder.JSONDecodeError: # intercept if error is made 
        check_ListIsDone = True # end of tickets changed to true
        print("ERROR PULLING TICKETS/END OF TICKETS DETECTED")

    else: # if list of Zohodesk tickets is recieved 
        counter_TicketCell = 0 # counter to help iterate through each cell in list of tickets 
        while counter_TicketCell < len(request_ListTickets['data']):
            dict_ListTickets = request_ListTickets['data'][counter_TicketCell] # grab dictionary containing redstor account's info and put into a new dictionary 
            dict_CopyOfListTickets = dict_ListTickets.copy() # create a copy of dictRedstorAccount
            list_AllTickets.append(dict_CopyOfListTickets) # add the copy of dictRedstorAccount to the list of filtered redstor accounts
            counter_TicketCell += 1
        print("TOTAL TICKETS APPENDED", len(list_AllTickets))

        param_from += 100
    




print(" \n \n " + "***SORTING THROUGH FILTERED BACKUPS FOR FAILED BACKUPS OR BACKUPS WITH ERRORS***" + " \n \n ")
# Sorting between failed/completed backups
counter_countTotalExistingTickets = 0
counter_CreatedTickets = 0 # counter for total created tickets
counter_Redstor = 0 # counter for iterating through redstor accounts
counter_TotalBackupsDetected = 0 # counter for total backup detected
check_ExistingTicket = False # boolean for whether existing ticket of redstor account is found or not
list_ExistingTickets = []
while counter_Redstor < len(filtered_request_Accounts): # while counter is less than length of list of filtered accounts

    # Reset counter to run through tickets 
    counter_ZohoDesk = 0 

    # Variables storing values for last backup date
    value_LastBackupDateAndTime = filtered_request_Accounts[counter_Redstor]['LastBackupDate'] # Pulls date and time of last backup performed as a string value
    value_LastBackupYear = int(value_LastBackupDateAndTime[0:4]) # Pulls year from value_LastBackupDateAndTime as integer 
    value_LastBackupMonth = int(value_LastBackupDateAndTime[5:7]) # Pulls month from value_LastBackupDateAndTime as integer 
    value_LastBackupDay = int(value_LastBackupDateAndTime[8:10]) # Pulls day from value_LastBackupDateAndTime as integer 
    
    # Variables storing values for todays date
    value_TodaysDate = str(date.today()) # Pulls today's date as a string
    value_TodaysYear = int(value_TodaysDate[0:4]) # Pulls year from value_TodaysDate as integer 
    value_TodaysMonth = int(value_TodaysDate[5:7]) # Pulls month from value_TodaysDate as integer 
    value_TodaysDay = int(value_TodaysDate[8:10]) # Pulls day from value_TodaysDate as integer

    # Variables storing values for todays date - backup date
    value_YearsFromLastBackup = value_TodaysYear - value_LastBackupYear # Total year(s) elapsed since last backup
    value_MonthsFromLastBackup = value_TodaysMonth - value_LastBackupMonth # Total month(s) elapsed since last backup
    value_DaysFromLastBackup = value_TodaysDay - value_LastBackupDay # Total day(s) elapsed since last backup
    
    #**************************************************************************************************
    # within this section is the body that will be sent to zohodesk to create a new ticket
    # anything that is within the body can be manipulated EXCEPT THE GUID WHICH MUST BE KEPT WITHIN THE
    # VERY END OF THE SUBJECT AS THE PROGRAM WILL SEARCH FOR THE GUID IN THAT POSITION LATER TO PREVENT
    # COPIES OF ALREADY EXISTING TICKETS.    
    #**************************************************************************************************
    # Set new variable values for redstor account information
    account_BackupGroup = (filtered_request_Accounts[counter_Redstor]['BackupGroup'])
    account_AccountName = filtered_request_Accounts[counter_Redstor]['AccountName']
    account_Guid = filtered_request_Accounts[counter_Redstor]['Guid']
    body = {
            'subject': f'*API-BOT* {account_AccountName} {account_BackupGroup} Guid: {account_Guid}',
            'departmentId': '605888000000006907',
            'contactId': '605888000000169029',
            'description': 'this is the description',
            #'productId': 'Redstor', 
            'priority': 'Medium',
            'category': 'Production',
            'subCategory': 'Redstor',
            'classification': 'Monitoring',
            'channel': 'API Bot'
            }
    




    #COUNTS ALL EXISTING TICKETS 
    counter_findingTotalExistingTickets = 0
    while counter_findingTotalExistingTickets < len(list_AllTickets): # while counter is less than length of list of tickets and if matching ticket hasn't been found yet
        param_CellWithGuid = convert(list_AllTickets[counter_findingTotalExistingTickets]['subject']) # splits the subject of a ticket for later use to get GUID 
        if filtered_request_Accounts[counter_Redstor]['AccountName'] == 'ACR-RRL-RODC':
            if list_AllTickets[counter_findingTotalExistingTickets]['ticketNumber'] == '4880':
                print (filtered_request_Accounts[counter_Redstor]['Guid'])
                print (param_CellWithGuid[(len(param_CellWithGuid) - 1)])
        if filtered_request_Accounts[counter_Redstor]['Guid'] == param_CellWithGuid[(len(param_CellWithGuid) - 1)]: # if redstor account guid value does not match guid value found on ticket subject
            dict_RedstorAccount = filtered_request_Accounts[counter_Redstor]['AccountName'] # grab dictionary containing redstor account's info and put into a new dictionary 
            list_ExistingTickets.append(dict_RedstorAccount) # add the copy of dictRedstorAccount to the list of filtered redstor accounts
            counter_countTotalExistingTickets += 1
            counter_findingTotalExistingTickets += 1
        
        else:
            counter_findingTotalExistingTickets += 1





    print("ACCOUNT #", counter_Redstor + 1)
    # Checking that backup has backed up within 3 days of previous one'
    if (value_YearsFromLastBackup == 0 and value_MonthsFromLastBackup == 0 and value_DaysFromLastBackup < 3) and (filtered_request_Accounts[counter_Redstor]['LastBackupMessage'] == "Completed with errors"): 
        print("BACKUP COMPLETED WITH ERRORS DETECTED")
        counter_TotalBackupsDetected += 1
        # Scanning for already existing ticket for that Redstor account
        while counter_ZohoDesk < len(list_AllTickets) and check_ExistingTicket == False: # while counter is less than length of list of tickets and if matching ticket hasn't been found yet
            param_CellWithGuid = convert(list_AllTickets[counter_ZohoDesk]['subject']) # splits the subject of a ticket for later use to get GUID 
            if filtered_request_Accounts[counter_Redstor]['Guid'] == param_CellWithGuid[(len(param_CellWithGuid) - 1)]: # if redstor account guid value does not match guid value found on ticket subject
                check_ExistingTicket = True # classify as existing ticket
                print ("REDSTOR GUID:  ", filtered_request_Accounts[counter_Redstor]['Guid'])
                print ("ZOHODESK GUID: ", param_CellWithGuid[(len(param_CellWithGuid) - 1)])
                print("***EXISTING TICKET FOUND***")
                print(filtered_request_Accounts[counter_Redstor]['AccountName'])
                print("'TIME ELAPSED:'", value_YearsFromLastBackup, "year(s),", value_MonthsFromLastBackup, "month(s),",value_DaysFromLastBackup, "day(s)")
                print(filtered_request_Accounts[counter_Redstor]['LastBackupMessage'])
                print(" \n \n ")
                # Here code will update existing ticket 
            else:
                counter_ZohoDesk += 1 # iterate counter to scan next ticket
                #print(counter_ZohoDesk)

        if counter_ZohoDesk == len(list_AllTickets) and check_ExistingTicket == False: # if every ticket has been checked and no existing ticket is found
            time.sleep (10)
            request_CreateTicket = requests.post("https://desk.zoho.com/api/v1/tickets", data = json.dumps(body), headers = headers) # send API request to zohodesk to create ticket with info found in body
            counter_CreatedTickets += 1
            print("---EXISTING TICKET NOT FOUND---")
            print(filtered_request_Accounts[counter_Redstor]['AccountName'])
            print("'TIME ELAPSED:'", value_YearsFromLastBackup, "year(s),", value_MonthsFromLastBackup, "month(s),",value_DaysFromLastBackup, "day(s)")
            print(filtered_request_Accounts[counter_Redstor]['LastBackupMessage'])
            print("TICKET CREATED")
            print("TICKET API REQUEST RESPONSE CODE:", request_CreateTicket)
            print(" \n \n ")


        # if ticket update occurred
        if check_ExistingTicket == True: # if check was changed to true
            check_ExistingTicket = False # reset the check to false 





    #if  (value_YearsFromLastBackup != 0 or value_MonthsFromLastBackup != 0 or value_DaysFromLastBackup >= 3) and ((filtered_request_Accounts[counter_Redstor]['LastBackupMessage'] == "Successful") or (filtered_request_Accounts[counter_Redstor]['LastBackupMessage'] == "Completed with errors"))
    # Checking that backups not completed for more than 3 days of previous one and last backup message 'Successful'
    if (value_YearsFromLastBackup != 0 or value_MonthsFromLastBackup != 0 or value_DaysFromLastBackup >= 3): 
        print("OLD BACKUP DETECTED")
        counter_TotalBackupsDetected += 1
        # Scanning for already existing ticket for that Redstor account
        while counter_ZohoDesk < len(list_AllTickets) and check_ExistingTicket == False: # while counter is less than length of list of tickets and if matching ticket hasn't been found yet
            param_CellWithGuid = convert(list_AllTickets[counter_ZohoDesk]['subject']) # splits the subject of a ticket for later use to get GUID
            if filtered_request_Accounts[counter_Redstor]['Guid'] == param_CellWithGuid[(len(param_CellWithGuid) - 1)]: # if redstor account guid value does not match guid value found on ticket subject
                check_ExistingTicket = True # classify as existing ticket
                print ("REDSTOR GUID:  ", filtered_request_Accounts[counter_Redstor]['Guid'])
                print ("ZOHODESK GUID: ", param_CellWithGuid[(len(param_CellWithGuid) - 1)])
                print("***EXISTING TICKET FOUND***")
                print(filtered_request_Accounts[counter_Redstor]['AccountName'])
                print("'TIME ELAPSED:'", value_YearsFromLastBackup, "year(s),", value_MonthsFromLastBackup, "month(s),",value_DaysFromLastBackup, "day(s)")
                print(filtered_request_Accounts[counter_Redstor]['LastBackupMessage'])
                print(" \n \n ")
                # Here code will update existing ticket 
            else:
                counter_ZohoDesk += 1 # iterate counter to scan next ticket
                #print(counter_ZohoDesk)
        
        
        if counter_ZohoDesk == len(list_AllTickets) and check_ExistingTicket == False: # if every ticket has been checked and no existing ticket is found
            time.sleep (10)
            request_CreateTicket = requests.post("https://desk.zoho.com/api/v1/tickets", data = json.dumps(body), headers = headers) # send API request to zohodesk to create ticket with info found in body
            counter_CreatedTickets += 1
            print("---EXISTING TICKET NOT FOUND---")
            print(filtered_request_Accounts[counter_Redstor]['AccountName'])
            print("'TIME ELAPSED:'", value_YearsFromLastBackup, "year(s),", value_MonthsFromLastBackup, "month(s),",value_DaysFromLastBackup, "day(s)")
            print(filtered_request_Accounts[counter_Redstor]['LastBackupMessage'])
            print("TICKET CREATED")
            print("TICKET API REQUEST RESPONSE CODE:", request_CreateTicket)
            print(" \n \n ")

        # if ticket update occurred
        if check_ExistingTicket == True: # if check was changed to true
            check_ExistingTicket = False # reset the check to false 
            
    
    
    # Iterate loop
    counter_Redstor += 1
print("COMPLETED WITH ERRORS/FAILED ACCOUNTS DETECTED:", counter_TotalBackupsDetected)
print("TOTAL EXISTING TICKETS", counter_countTotalExistingTickets)
print("NEW TICKETS CREATED:", counter_CreatedTickets)
