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





#***REDSTOR API REQUEST FOR ALL REDSTOR ACCOUNTS***
# SP = 'https://api.pro.redstor.com'
#  Set your login details ! Defaulting on prov portal login
s = requests.Session()
#s.auth = ('shreports', 'KickingMemory2021')
s.auth = ('sean.swanepoel', '$wanep03!')
# Recieve list of dictionaries including all Accounts with BackupGroup, AccountName, LastBackupMessage, LastBackupStatus
request_Accounts = s.get('https://api.pro.redstor.com/api/odata/Accounts').json()['value']





#***FILTERING OF REDSTOR ACCOUNTS***
# Converting list of all redstor accounts into a filtered version 
counter_request_Accounts = 0 # counter to iterate through each redstor account's information
filtered_request_Accounts = [] # declaration of list which will be filled with filtered redstor accounts
while counter_request_Accounts < (len(request_Accounts)): # while counter is less than length of list of redstor accounts
    list_BackupGroup = convert2(request_Accounts[counter_request_Accounts]['BackupGroup']) # create temporary list to place the seperated path into
    length_list_BackupGroup = len(list_BackupGroup) # length of list_BackupGroup to help iterate through the contents later 
    counter_BackupGroup = 0 # counter to iterate through list_BackupGroup's cells for checks
    check_AgencyPartner = False # check for an agency partner account
    while counter_BackupGroup < length_list_BackupGroup: # while counter is less than length of list_BackupGroup
        if length_list_BackupGroup >= 4: # if length of list_BackupGroup is equal to or greater than 4
            if list_BackupGroup[3] == 'Agency Partners' and check_AgencyPartner == False: # then check if within path 'Agency Partners' is found
                check_AgencyPartner = True # classify redstor account in question as an agency partner
        counter_BackupGroup += 1 #iterate to scan next cell in list of backupgroup path
        
    if check_AgencyPartner == True and request_Accounts[counter_request_Accounts]['Active'] == True and request_Accounts[counter_request_Accounts]['LastBackupDate'] is not None: # if redstor account in question is an agency partner and classified as active
        dict_RedstorAccount = request_Accounts[counter_request_Accounts] # grab dictionary containing redstor account's info and put into a new dictionary 
        dict_copy = dict_RedstorAccount.copy() # create a copy of dictRedstorAccount
        filtered_request_Accounts.append(dict_copy) # add the copy of dictRedstorAccount to the list of filtered redstor accounts
        
    counter_request_Accounts += 1 #iterate to scan next cell in list of redstor accounts





#***ZOHO DESK API REQUEST FOR TICKETS***
# Grabbing required information for listing tickets and storing them in a variable
token_Refresh = "1000.9ee7878e462dce91ba93370cc8ae4c89.00605d5a1acbe96c72f5cebc59d385ab" # refresh token used to fetch new access token for access to zohodesk API requests, lasts forever
request_RefreshToken = requests.post(f'https://accounts.zoho.com/oauth/v2/token?refresh_token={token_Refresh}&client_id=1000.YDOPB4JT48NG4LP3V9VPKFINZIECIR&client_secret=1498df3bd8ab23e6d9e4b7fe742c6e7e663de67919&grant_type=refresh_token').json() # API request for new access token
token_Access = str(request_RefreshToken['access_token']) # grabbing just the access token from 
headers = {'orgId': ('751922355') , 'Authorization': f'Zoho-oauthtoken {token_Access}'}
request_ListTickets = requests.get("https://desk.zoho.com/api/v1/tickets?include=contacts,assignee,departments,team,isRead", headers = headers).json()





#***SORTING THROUGH FILTERED BACKUPS FOR FAILED BACKUPS OR BACKUPS WITH ERRORS***
# Sorting between failed/completed backups
counter_Redstor = 0
check_ExistingTicket = False
while counter_Redstor < len(filtered_request_Accounts): 
    




    # Reset counter to run through tickets 
    counter_ZohoDesk = 0

    # Set new variable values for redstor account information
    account_BackupGroup = (filtered_request_Accounts[counter_Redstor]['BackupGroup'])
    account_AccountName = filtered_request_Accounts[counter_Redstor]['AccountName']
    account_Guid = filtered_request_Accounts[counter_Redstor]['Guid']

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
    




    # Checking that backup has backed up within 3 days of previous one and last backup message is 'Completed with errors'
    if  (value_YearsFromLastBackup == 0 and value_MonthsFromLastBackup == 0 and value_DaysFromLastBackup < 3) and (filtered_request_Accounts[counter_Redstor]['LastBackupMessage'] == "Completed with errors"): 
        #("-----COMPLETED (WITH ERRORS) AND UP TO DATE BACKUP-----")
        #print("'TIME ELAPSED:'", value_YearsFromLastBackup, "year(s),", value_MonthsFromLastBackup, "month(s),",value_DaysFromLastBackup, "day(s)")

        # Scanning for already existing ticket for that Redstor account
        while counter_ZohoDesk < len(request_ListTickets['data']) and check_ExistingTicket == False: # while counter is less than length of list of tickets and if matching ticket hasn't been found yet
            if filtered_request_Accounts[counter_Redstor]['Guid'] == (convert(request_ListTickets['data'][counter_ZohoDesk]['subject'])[2]): # if redstor account guid value does not match guid value found on ticket subject
                check_ExistingTicket = True # classify as existing ticket
                # Here code will update existing ticket 
            else:
                counter_ZohoDesk += 1 # iterate counter to scan next ticket
                print(counter_ZohoDesk)
        print(check_ExistingTicket)

        if counter_ZohoDesk < len(filtered_request_Accounts) and check_ExistingTicket == False: # if every ticket has been checked and no existing ticket is found
            body = {
            'subject': f'*API-BOT* Guid: {account_Guid} {account_BackupGroup} {account_AccountName}',
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
            request_CreateTicket = requests.post("https://desk.zoho.com/api/v1/tickets", data = json.dumps(body), headers = headers) # send API request to zohodesk to create ticket with info found in body
        
        # if ticket update occurred
        if check_ExistingTicket == True: # if check was changed to true
            check_ExistingTicket = False # reset the check to false 
    




    # Checking that backups not completed for more than 3 days of previous one and last backup message 'Successful'
    if  (value_YearsFromLastBackup != 0 or value_MonthsFromLastBackup != 0 or value_DaysFromLastBackup >= 3) and ((filtered_request_Accounts[counter_Redstor]['LastBackupMessage'] == "Successful") or (filtered_request_Accounts[counter_Redstor]['LastBackupMessage'] == "Completed with errors")): 
        #print("*****FAILED OR OLD BACKUP DETECTED*****")
        #print("'TIME ELAPSED:'", value_YearsFromLastBackup, "year(s),", value_MonthsFromLastBackup, "month(s),",value_DaysFromLastBackup, "day(s)")

        # Scanning for already existing ticket for that Redstor account
        while counter_ZohoDesk < len(request_ListTickets['data']) and check_ExistingTicket == False: # while counter is less than length of list of tickets and if matching ticket hasn't been found yet
            if filtered_request_Accounts[counter_Redstor]['Guid'] == (convert(request_ListTickets['data'][counter_ZohoDesk]['subject'])[2]): # if redstor account guid value does not match guid value found on ticket subject
                check_ExistingTicket = True # classify as existing ticket
                # Here code will update existing ticket 
            else:
                counter_ZohoDesk += 1 # iterate counter to scan next ticket
                print(counter_ZohoDesk)
        print(check_ExistingTicket)

        if counter_ZohoDesk < len(filtered_request_Accounts) and check_ExistingTicket == False: # if every ticket has been checked and no existing ticket is found
            body = {
            'subject': f'*API-BOT* Guid: {account_Guid} {account_BackupGroup} {account_AccountName}',
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
            request_CreateTicket = requests.post("https://desk.zoho.com/api/v1/tickets", data = json.dumps(body), headers = headers) # send API request to zohodesk to create ticket with info found in body

        # if ticket update occurred
        if check_ExistingTicket == True: # if check was changed to true
            check_ExistingTicket = False # reset the check to false 
            
    
    
    # Iterate loop
    counter_Redstor += 1


print ("Sucessful!")