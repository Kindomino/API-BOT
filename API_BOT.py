from pip._vendor import requests
from datetime import date
import pprint, time, json


#***FUNCTIONS***
# Python code to convert string to list
def convertBySpace(string):
    li = list(string.split(" "))
    return li
# Python code to convert backup group path to list
def convertByDoubleBackslash(string):
    li = list(string.split("\\"))
    return li
# Python3 program to Split string into characters
def convertByChar(word):
    return [char for char in word]
# Python code to convert days since last backup to list
def convertByComma(string):
    li = list(string.split(","))
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
param_Skip = 0
counter_AccountsScanned = 0
counter_CellPositionWithinList = 0
counter_AgencyPartners = 0
counter_VSG = 0
counter_S4iSystems = 0 
list_AllRedstorAccounts = [] 
while len(request_Accounts) == 1000: 
    request_Accounts = s.get(f'https://api.pro.redstor.com/api/odata/Accounts?$skip={param_Skip}').json()['value'] 
    time.sleep(10)
    counter_AccountsAdded = 0 
    while counter_CellPositionWithinList < (len(request_Accounts)):
        list_BackupGroup = convertByDoubleBackslash(request_Accounts[counter_CellPositionWithinList]['BackupGroup']) 
        length_list_BackupGroup = len(list_BackupGroup)
        # scans through redstor account path for agency partners  
        counter_BackupGroup = 0 
        check_AgencyPartner = False
        while counter_BackupGroup < length_list_BackupGroup: 
            if list_BackupGroup[counter_BackupGroup] == 'Agency Partners' and check_AgencyPartner == False: # LINE OF CODE WITHIN DOCUMENTATION ABOVE, checks if within path 'Agency Partners' is found
                check_AgencyPartner = True 
                counter_AgencyPartners += 1
            counter_BackupGroup += 1
        # scans through redstor account path for vsg
        counter_BackupGroup = 0
        check_VSG = False
        while counter_BackupGroup < length_list_BackupGroup: 
            if list_BackupGroup[counter_BackupGroup] == 'VSG' and check_VSG == False: # LINE OF CODE WITHIN DOCUMENTATION ABOVE, checks if within path 'Agency Partners' is found
                check_VSG = True
                counter_VSG += 1
            counter_BackupGroup += 1
        # scans through redstor account path for s4i
        counter_BackupGroup = 0
        check_S4iSystems = False
        while counter_BackupGroup < length_list_BackupGroup: 
            if list_BackupGroup[counter_BackupGroup] == 'S4i Systems' and check_S4iSystems == False: # LINE OF CODE WITHIN DOCUMENTATION ABOVE, checks if within path 'Agency Partners' is found
                check_S4iSystems = True
                counter_S4iSystems += 1 
            counter_BackupGroup += 1     
        # checks if redstor account in question is an agency partner and classified as active
        if (check_AgencyPartner == True or check_VSG == True or check_S4iSystems == True) and request_Accounts[counter_CellPositionWithinList]['Active'] == True and request_Accounts[counter_CellPositionWithinList]['LastBackupDate'] is not None:
            dict_RedstorAccount = request_Accounts[counter_CellPositionWithinList]
            copy_RedstorAccount = dict_RedstorAccount.copy() 
            list_AllRedstorAccounts.append(copy_RedstorAccount) 
            counter_AccountsAdded += 1

        
        counter_CellPositionWithinList += 1
        counter_AccountsScanned += 1 
    
    counter_CellPositionWithinList = 0
    # next 1000 redstor accounts  
    param_Skip += 1000 
    print ("REDSTOR ACCOUNTS SCANNED: ", counter_AccountsScanned)
    print ("REDSTOR ACCOUNTS ADDED: ", counter_AccountsAdded)
print("TOTAL ACCOUNTS ADDED: ", len(list_AllRedstorAccounts))
print("TOTAL AGENCY PARTNER ACCOUNTS ADDED: ", counter_AgencyPartners)
print("TOTAL VSG ACCOUNTS ADDED: ", counter_VSG)
print("TOTAL S4I SYSTEMS ACCOUNTS ADDED: ", counter_S4iSystems)






#**************************************************************************************************
# to manipulate token_refresh for your own zohodesk enviroment setup a refresh token beforehand on 
# postman and grab orgID within variable 'headers' by heading onto your zohodesk enviroment and
# select the settings tab on the top right, select 'API' under 'DEVELOPER SPACE' and orgId will be
# found at the bottom of the page                 
#**************************************************************************************************
#***ZOHO DESK API REQUEST FOR TICKETS***
# Grabbing required information for listing tickets and storing them in a variable

#ZOHODESK FOR PROTOS ENVIROMENT
# refresh token used to fetch new access token for access to zohodesk API requests, lasts forever
token_Refresh = "1000.fa7c3477d27a33d4e9df3441236aaf1e.24367a4034451565c64eecc13eda4d75"
# client id used to link API request to your zohodesk enviroment
client_Id = "1000.C800QHYEAC2X5ONRKWESJMLL1S6V3F"
# client secret used to link API request to your zohodesk enviroment
client_Secret = "e5a46872f4e7f126e2f066a4ec30c54be6efc6c1c4"
# API request for access token
request_RefreshToken = requests.post(f'https://accounts.zoho.com/oauth/v2/token?refresh_token={token_Refresh}&client_id={client_Id}&client_secret={client_Secret}&grant_type=refresh_token').json()
# grabbing just the access token from API request
token_Access = str(request_RefreshToken['access_token'])
# headers for any further Zohodesk API requests
headers = {'orgId': ('732503526') , 'Authorization': f'Zoho-oauthtoken {token_Access}'}

#ZOHODESK FOR PERSONAL ENVIROMENT
#token_Refresh = "1000.9ee7878e462dce91ba93370cc8ae4c89.00605d5a1acbe96c72f5cebc59d385ab" # refresh token used to fetch new access token for access to zohodesk API requests, lasts forever
#client_Id = "1000.YDOPB4JT48NG4LP3V9VPKFINZIECIR" # client id used to link API request to your zohodesk enviroment
#client_Secret = "1498df3bd8ab23e6d9e4b7fe742c6e7e663de67919" # client secret used to link API request to your zohodesk enviroment
#request_RefreshToken = requests.post(f'https://accounts.zoho.com/oauth/v2/token?refresh_token={token_Refresh}&client_id={client_Id}&client_secret={client_Secret}&grant_type=refresh_token').json() # API request for access token
#token_Access = str(request_RefreshToken['access_token']) # grabbing just the access token from API request
#headers = {'orgId': ('751922355') , 'Authorization': f'Zoho-oauthtoken {token_Access}'} # headers for any further Zohodesk API requests 





#**************************************************************************************************
# Nothing will need to be changed in this section 
#**************************************************************************************************
print(" \n \n " + "***GRABBING ALL TICKETS AND PLACING THEM IN LIST***")
# from parameter in request_ListTickets API request
param_from = 0 
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
    



# Sorting between failed/completed backups
print(" \n \n " + "***SORTING THROUGH FILTERED BACKUPS FOR FAILED BACKUPS OR BACKUPS WITH ERRORS***" + " \n \n ")
counter_CountTotalExistingTickets = 0
counter_CreatedTickets = 0 
counter_RedstorAccount = 0 # counter for iterating through redstor accounts
counter_TotalBackupsDetected = 0
counter_TotalOldOrFailedBackups = 0
counter_TotalCompletedWithErrors = 0 
check_ExistingTicket = False # boolean for whether existing ticket of redstor account is found or not
check_UpdatedLBM = False
list_ExistingTickets = []
list_OldOrFailedAccounts = []
while counter_RedstorAccount < len(list_AllRedstorAccounts):



    # Reset counter to run through tickets 
    counter_ZohoDesk = 0 



    # Variables storing values for last backup date
    value_LastBackupDateAndTime = list_AllRedstorAccounts[counter_RedstorAccount]['LastBackupDate'] # Pulls date and time of last backup performed as a string value
    value_LastBackupYear = int(value_LastBackupDateAndTime[0:4]) # Pulls year from value_LastBackupDateAndTime as integer
    value_LastBackupMonth = str(value_LastBackupDateAndTime[5:7]) # Pulls month from value_LastBackupDateAndTime as str 
    value_TempLastBackupMonth = convertByChar(str(value_LastBackupDateAndTime[5:7]))
    # Removing any unnecessary zeros from date i.e. 2001-01-05 -> 2001-1-5
    if value_TempLastBackupMonth[0] == '0':
        value_LastBackupMonth = int(value_LastBackupMonth[1])
    else:
        value_LastBackupMonth = int(value_LastBackupMonth)
    value_LastBackupDay = str(value_LastBackupDateAndTime[8:10]) # Pulls day from value_LastBackupDateAndTime as integer 
    value_TempLastBackupDay = convertByChar(str(value_LastBackupDateAndTime[8:10]))
    if value_TempLastBackupDay[0] == '0':
        value_LastBackupDay = int(value_LastBackupDay[1])
    else:
        value_LastBackupDay = int(value_LastBackupDay)



    # Variables storing values for todays date
    value_TodaysDate = str(date.today()) # Pulls today's date as a string
    value_TodaysYear = int(value_TodaysDate[0:4]) # Pulls year from value_TodaysDate as integer 
    value_TodaysMonth = str(value_TodaysDate[5:7]) # Pulls month from value_TodaysDate as str 
    value_TempTodaysMonth = convertByChar(str(value_TodaysDate[5:7]))
    # Removing any unnecessary zeros from date i.e. 2001-01-05 -> 2001-1-5
    if value_TempTodaysMonth[0] == '0':
        value_TodaysMonth = int(value_TodaysMonth[1])
    else:
        value_TodaysMonth = int(value_TodaysMonth)
    value_TodaysDay = str(value_TodaysDate[8:10]) # Pulls day from value_TodaysDate as integer
    value_TempTodaysDay = convertByChar(str(value_TodaysDate[8:10]))
    if value_TempTodaysDay[0] == '0':
        value_TodaysDay = int(value_TodaysDay[1])
    else:
        value_TodaysDay = int(value_TodaysDay)
        


    # Variables storing values for todays date - backup date
    #value_YearsFromLastBackup = value_TodaysYear - value_LastBackupYear # Total year(s) elapsed since last backup
    #value_MonthsFromLastBackup = value_TodaysMonth - value_LastBackupMonth # Total month(s) elapsed since last backup
    #value_DaysFromLastBackup = value_TodaysDay - value_LastBackupDay # Total day(s) elapsed since last backup



    # Variables calculating days from todays date to last backup date 
    date_Today = date(value_TodaysYear, value_TodaysMonth, value_TodaysDay)
    date_LastBackup = date(value_LastBackupYear, value_LastBackupMonth, value_LastBackupDay)
    value_DaysFromLastBackup = str(date_Today - date_LastBackup)



    #**************************************************************************************************
    # within this section is the body that will be sent to zohodesk to create a new ticket
    # anything that is within the body can be manipulated EXCEPT THE GUID WHICH MUST BE KEPT WITHIN THE
    # VERY END OF THE SUBJECT AS THE PROGRAM WILL SEARCH FOR THE GUID IN THAT POSITION LATER TO PREVENT
    # COPIES OF ALREADY EXISTING TICKETS.    
    #**************************************************************************************************
    # Set new variable values for redstor account information
    account_BackupGroup = (list_AllRedstorAccounts[counter_RedstorAccount]['BackupGroup'])
    account_AccountName = list_AllRedstorAccounts[counter_RedstorAccount]['AccountName']
    account_Guid = list_AllRedstorAccounts[counter_RedstorAccount]['Guid']
    account_LastBackupMessage = list_AllRedstorAccounts[counter_RedstorAccount]['LastBackupMessage']
    value_GroupLocation = (len(convertByDoubleBackslash(account_BackupGroup))) - 1
    account_Group = (convertByDoubleBackslash(account_BackupGroup))[value_GroupLocation]
    
    print(account_Group)


    #COUNTS ALL EXISTING TICKETS 
    counter_findingTotalExistingTickets = 0
    while counter_findingTotalExistingTickets < len(list_AllTickets): # while counter is less than length of list of tickets and if matching ticket hasn't been found yet
        param_CellWithGuid = convertBySpace(list_AllTickets[counter_findingTotalExistingTickets]['subject']) # splits the subject of a ticket for later use to get GUID 
        #if list_AllRedstorAccounts[counter_RedstorAccount]['AccountName'] == 'ACR-RRL-RODC':
        #    if list_AllTickets[counter_findingTotalExistingTickets]['ticketNumber'] == '4880':
        #        print (list_AllRedstorAccounts[counter_RedstorAccount]['Guid'])
        #        print (param_CellWithGuid[(len(param_CellWithGuid) - 1)])
        if list_AllRedstorAccounts[counter_RedstorAccount]['Guid'] == param_CellWithGuid[(len(param_CellWithGuid) - 1)]: # if redstor account guid value does not match guid value found on ticket subject
            dict_RedstorAccount = list_AllRedstorAccounts[counter_RedstorAccount]['AccountName'] # grab dictionary containing redstor account's info and put into a new dictionary 
            list_ExistingTickets.append(dict_RedstorAccount) # add the copy of dictRedstorAccount to the list of filtered redstor accounts
            counter_CountTotalExistingTickets += 1
            counter_findingTotalExistingTickets += 1
        
        else:
            counter_findingTotalExistingTickets += 1



    

    print("ACCOUNT #", counter_RedstorAccount + 1)
    print(date_Today)
    print(date_LastBackup)
    print(value_DaysFromLastBackup)
    # Checking that backup has backed up within 3 days of previous one'
    if (value_DaysFromLastBackup == '1 day, 0:00:00' or value_DaysFromLastBackup == '2 days, 0:00:00' or value_DaysFromLastBackup == '-1 day, 0:00:00' or value_DaysFromLastBackup == '0:00:00') and (list_AllRedstorAccounts[counter_RedstorAccount]['LastBackupMessage'] == "Completed with errors"): 
        print(list_AllRedstorAccounts[counter_RedstorAccount]['LastBackupMessage'])
        print("BACKUP COMPLETED WITH ERRORS DETECTED")
        counter_TotalBackupsDetected += 1
        counter_TotalCompletedWithErrors += 1
        # Scanning for already existing ticket for that Redstor account
        while counter_ZohoDesk < len(list_AllTickets) and check_ExistingTicket == False: # while counter is less than length of list of tickets and if matching ticket hasn't been found yet
            param_CellWithGuid = convertBySpace(list_AllTickets[counter_ZohoDesk]['subject']) # splits the subject of a ticket for later use to get GUID 
            if list_AllRedstorAccounts[counter_RedstorAccount]['Guid'] == param_CellWithGuid[(len(param_CellWithGuid) - 1)]: # if redstor account guid value does match guid value found on ticket subject
                check_ExistingTicket = True # classify as existing ticket
                print ("REDSTOR GUID:  ", list_AllRedstorAccounts[counter_RedstorAccount]['Guid'])
                print ("ZOHODESK GUID: ", param_CellWithGuid[(len(param_CellWithGuid) - 1)])
                print("***EXISTING TICKET FOUND***")
                print(list_AllRedstorAccounts[counter_RedstorAccount]['AccountName'])
                print("'TIME ELAPSED:'", value_DaysFromLastBackup)
                print(list_AllRedstorAccounts[counter_RedstorAccount]['LastBackupMessage'])
                print(list_AllTickets[counter_ZohoDesk]['status'])
                if list_AllTickets[counter_ZohoDesk]['status'] != 'Closed':    
                    print('UPDATING TICKET...')

                    # Updating API-BOT generated ticket with updated description
                    time.sleep (10)
                    #if param_CellWithGuid[0] == '*API-BOT*':
                    #    body_UpdateTicket = {
                    #        'description': f'BACKUP COMPLETED WITH ERRORS:<br>PATH: {account_BackupGroup}<br>LAST BACKUP MESSAGE:{account_LastBackupMessage}<br>LAST BACKUP DATE (MM/DD/YYYY): {value_LastBackupMonth}-{value_LastBackupDay}-{value_LastBackupYear}'
                    #    }
                    #    param_TicketId = list_AllTickets[counter_ZohoDesk]['id']
                    #    request_UpdateTicket = requests.patch(f"https://desk.zoho.com/api/v1/tickets/{param_TicketId}", data = json.dumps(body_UpdateTicket), headers = headers)
                    #print("TICKET API REQUEST RESPONSE CODE:", request_UpdateTicket)
                    #if param_CellWithGuid[0] == '*API-BOT*':
                    body_CreateComment = {
                    "isPublic" : "false",
                    "content" : f'<b>BACKUP COMPLETED WITH ERRORS DETECTED:</b><br><b>PATH:</b> {account_BackupGroup}<br><b>LAST BACKUP MESSAGE:</b> {account_LastBackupMessage}<br><b>LAST BACKUP DATE (MM/DD/YYYY):</b> {value_LastBackupMonth}-{value_LastBackupDay}-{value_LastBackupYear}'
                    }
                    param_TicketId = list_AllTickets[counter_ZohoDesk]['id']
                    request_CreateComment = requests.post(f"https://desk.zoho.com/api/v1/tickets/{param_TicketId}/comments", data = json.dumps(body_CreateComment), headers = headers)
                    print("CREATE COMMENT API REQUEST RESPONSE CODE:", request_CreateComment)
                    print(" \n \n ")
                if list_AllTickets[counter_ZohoDesk]['status'] == 'Closed':
                    check_ExistingTicket = False
                    print('~~~~~EXISTING CLOSED TICKET DETECTED~~~~~')
                    counter_ZohoDesk += 1

            else:
                counter_ZohoDesk += 1 # iterate counter to scan next ticket

        # Creating new ticket
        if counter_ZohoDesk == len(list_AllTickets) and check_ExistingTicket == False: # if every ticket has been checked and no existing ticket is found
            body_CreateTicket = {
            'subject': f'BACKUP COMPLETED WITH ERRORS • {account_Group}/{account_AccountName} • LBM: {account_LastBackupMessage} • GUID: {account_Guid}',
            'departmentId': '562761000004050121',
            'contactId': '562761000004216013',
            'assigneeId': '562761000000389001',
            'email': 'drmonitoring@protostechnologiesgroup.zohodesk.com',
            'description': f'<b>BACKUP COMPLETED WITH ERRORS DETECTED:</b><br><b>PATH:</b> {account_BackupGroup}<br><b>LAST BACKUP MESSAGE:</b> {account_LastBackupMessage}<br><b>LAST BACKUP DATE (MM/DD/YYYY):</b> {value_LastBackupMonth}-{value_LastBackupDay}-{value_LastBackupYear}',
            #'productId': 'Redstor', 
            'priority': 'Medium',
            'category': 'Production',
            'subCategory': 'Redstor',
            'classification': 'Monitoring',
            'channel': 'API Bot'
            }

            if len(convertByChar(body_CreateTicket['subject'])) > 160:
                check_UpdatedLBM = True
                value_SubjectLenExceedsBy = len(convertByChar(body_CreateTicket['subject'])) - 160
                account_NewLastBackupMessage = ''.join(convertByChar(account_LastBackupMessage)[0:len(convertByChar(account_LastBackupMessage)) - value_SubjectLenExceedsBy])
                body_CreateTicket = {
                'subject': f'BACKUP COMPLETED WITH ERRORS • {account_Group}/{account_AccountName} • LBM: {account_NewLastBackupMessage} • GUID: {account_Guid}',
                'departmentId': '562761000004050121',
                'contactId': '562761000004216013',
                'assigneeId': '562761000000389001',
                'email': 'drmonitoring@protostechnologiesgroup.zohodesk.com',
                'description': f'<b>BACKUP COMPLETED WITH ERRORS DETECTED:</b><br><b>PATH:</b> {account_BackupGroup}<br><b>LAST BACKUP MESSAGE:</b> {account_LastBackupMessage}<br><b>LAST BACKUP DATE (MM/DD/YYYY):</b> {value_LastBackupMonth}-{value_LastBackupDay}-{value_LastBackupYear}',
                #'productId': 'Redstor', 
                'priority': 'Medium',
                'category': 'Production',
                'subCategory': 'Redstor',
                'classification': 'Monitoring',
                'channel': 'API Bot'
                }

            counter_CreatedTickets += 1
            print ("REDSTOR GUID:  ", list_AllRedstorAccounts[counter_RedstorAccount]['Guid'])
            print("---EXISTING TICKET NOT FOUND---")
            print(list_AllRedstorAccounts[counter_RedstorAccount]['AccountName'])
            print("'TIME ELAPSED:'", value_DaysFromLastBackup)
            print(list_AllRedstorAccounts[counter_RedstorAccount]['LastBackupMessage'])
            print("LAST BACKUP MESSAGE LENGTH: ", len(convertByChar(body_CreateTicket['subject'])))
            if check_UpdatedLBM == True:
                check_UpdatedLBM = False
                print("LAST BACKUP MESSAGE UPDATED")
            print("TICKET IS BEING CREATED...")
            time.sleep (10)
            request_CreateTicket = requests.post("https://desk.zoho.com/api/v1/tickets", data = json.dumps(body_CreateTicket), headers = headers) # send API request to zohodesk to create ticket with info found in body
            print("TICKET API REQUEST RESPONSE CODE:", request_CreateTicket)
            pprint.pprint(body_CreateTicket)
            print(" \n \n ")

        # if ticket update occurred
        if check_ExistingTicket == True: # if check was changed to true
            check_ExistingTicket = False # reset the check to false 





    #if  (value_YearsFromLastBackup != 0 or value_MonthsFromLastBackup != 0 or value_DaysFromLastBackup >= 3) and ((list_AllRedstorAccounts[counter_RedstorAccount]['LastBackupMessage'] == "Successful") or (list_AllRedstorAccounts[counter_RedstorAccount]['LastBackupMessage'] == "Completed with errors"))
    # Checking that backups not completed for more than 3 days of previous one and last backup message 'Successful'
    if value_DaysFromLastBackup != '1 day, 0:00:00' and value_DaysFromLastBackup != '2 days, 0:00:00' and value_DaysFromLastBackup != '-1 day, 0:00:00' and value_DaysFromLastBackup != '0:00:00': 
        print("OLD/FAILED BACKUP DETECTED")
        dict_OldOrFailedBackupAccountName = list_AllRedstorAccounts[counter_RedstorAccount]['AccountName'] # grab dictionary containing redstor account's info and put into a new dictionary 
        list_OldOrFailedAccounts.append(dict_OldOrFailedBackupAccountName)
        counter_TotalBackupsDetected += 1
        counter_TotalOldOrFailedBackups += 1
        # Scanning for already existing ticket for that Redstor account
        while counter_ZohoDesk < len(list_AllTickets) and check_ExistingTicket == False: # while counter is less than length of list of tickets and if matching ticket hasn't been found yet
            param_CellWithGuid = convertBySpace(list_AllTickets[counter_ZohoDesk]['subject']) # splits the subject of a ticket for later use to get GUID
            if list_AllRedstorAccounts[counter_RedstorAccount]['Guid'] == param_CellWithGuid[(len(param_CellWithGuid) - 1)]: # if redstor account guid value does match guid value found on ticket subject
                check_ExistingTicket = True # classify as existing ticket
                print ("REDSTOR GUID:  ", list_AllRedstorAccounts[counter_RedstorAccount]['Guid'])
                print ("ZOHODESK GUID: ", param_CellWithGuid[(len(param_CellWithGuid) - 1)])
                print("***EXISTING TICKET FOUND***")
                print(list_AllRedstorAccounts[counter_RedstorAccount]['AccountName'])
                print("'TIME ELAPSED:'", value_DaysFromLastBackup)
                print(list_AllRedstorAccounts[counter_RedstorAccount]['LastBackupMessage'])
                print(list_AllTickets[counter_ZohoDesk]['status'])
                if list_AllTickets[counter_ZohoDesk]['status'] != 'Closed':    
                    print('UPDATING TICKET...')
                    
                    # Updating API-BOT generated ticket with updated description and comment 
                    time.sleep (10)
                    #if param_CellWithGuid[0] == '*API-BOT*':
                    #    body_UpdateTicket = {
                    #        'description': f'OLD BACKUP:<br>PATH: {account_BackupGroup}<br>LAST BACKUP MESSAGE:{account_LastBackupMessage}<br>LAST BACKUP DATE (MM/DD/YYYY): {value_LastBackupMonth}-{value_LastBackupDay}-{value_LastBackupYear}'
                    #    }
                    #    param_TicketId = list_AllTickets[counter_ZohoDesk]['id']
                    #    request_UpdateTicket = requests.patch(f"https://desk.zoho.com/api/v1/tickets/{param_TicketId}", data = json.dumps(body_UpdateTicket), headers = headers)
                    #print("TICKET API REQUEST RESPONSE CODE:", request_UpdateTicket)
                    #if param_CellWithGuid[0] == '*API-BOT*':
                    body_CreateComment = {
                    "isPublic" : "false",
                    "content" : f'<b>OLD/FAILED BACKUP DETECTED:</b><br><b>PATH:</b> {account_BackupGroup}<br><b>LAST BACKUP MESSAGE:</b> {account_LastBackupMessage}<br><b>LAST BACKUP DATE (MM/DD/YYYY):</b> {value_LastBackupMonth}-{value_LastBackupDay}-{value_LastBackupYear}<br><b>TIME SINCE LAST BACKUP:</b> {(convertByComma(value_DaysFromLastBackup))[0]}'
                    }
                    param_TicketId = list_AllTickets[counter_ZohoDesk]['id']
                    request_CreateComment = requests.post(f"https://desk.zoho.com/api/v1/tickets/{param_TicketId}/comments", data = json.dumps(body_CreateComment), headers = headers)
                    print("CREATE COMMENT API REQUEST RESPONSE CODE:", request_CreateComment)
                    print(" \n \n ")
                if list_AllTickets[counter_ZohoDesk]['status'] == 'Closed':
                    check_ExistingTicket = False
                    print('~~~~~EXISTING CLOSED TICKET DETECTED~~~~~')
                    counter_ZohoDesk += 1

            else:
                counter_ZohoDesk += 1 # iterate counter to scan next ticket
        
        
        if counter_ZohoDesk == len(list_AllTickets) and check_ExistingTicket == False: # if every ticket has been checked and no existing ticket is found
            body_CreateTicket = {
            'subject': f'OLD/FAILED BACKUP • {account_Group}/{account_AccountName} • LBM: {account_LastBackupMessage} • GUID: {account_Guid}',
            'departmentId': '562761000004050121',
            'contactId': '562761000004216013',
            'assigneeId': '562761000000389001',
            'email': 'drmonitoring@protostechnologiesgroup.zohodesk.com',
            'description': f'<b>OLD/FAILED BACKUP DETECTED:</b><br><b>PATH:</b> {account_BackupGroup}<br><b>LAST BACKUP MESSAGE:</b> {account_LastBackupMessage}<br><b>LAST BACKUP DATE (MM/DD/YYYY):</b> {value_LastBackupMonth}-{value_LastBackupDay}-{value_LastBackupYear}<br><b>TIME SINCE LAST BACKUP:</b> {(convertByComma(value_DaysFromLastBackup))[0]}',
            #'productId': 'Redstor', 
            'priority': 'Medium',
            'category': 'Production',
            'subCategory': 'Redstor',
            'classification': 'Monitoring',
            'channel': 'API Bot'
            }
            
            if len(convertByChar(body_CreateTicket['subject'])) > 160:
                check_UpdatedLBM = True
                value_SubjectLenExceedsBy = len(convertByChar(body_CreateTicket['subject'])) - 160
                account_NewLastBackupMessage = ''.join(convertByChar(account_LastBackupMessage)[0:len(convertByChar(account_LastBackupMessage)) - value_SubjectLenExceedsBy])
                body_CreateTicket = {
                'subject': f'OLD/FAILED BACKUP • {account_Group}/{account_AccountName} • LBM: {account_NewLastBackupMessage} • GUID: {account_Guid}',
                'departmentId': '562761000004050121',
                'contactId': '562761000004216013',
                'assigneeId': '562761000000389001',
                'email': 'drmonitoring@protostechnologiesgroup.zohodesk.com',
                'description': f'<b>OLD/FAILED BACKUP DETECTED:</b><br><b>PATH:</b> {account_BackupGroup}<br><b>LAST BACKUP MESSAGE:</b> {account_LastBackupMessage}<br><b>LAST BACKUP DATE (MM/DD/YYYY):</b> {value_LastBackupMonth}-{value_LastBackupDay}-{value_LastBackupYear}',
                #'productId': 'Redstor', 
                'priority': 'Medium',
                'category': 'Production',
                'subCategory': 'Redstor',
                'classification': 'Monitoring',
                'channel': 'API Bot'
                }

            counter_CreatedTickets += 1
            print ("REDSTOR GUID:  ", list_AllRedstorAccounts[counter_RedstorAccount]['Guid'])
            print("---EXISTING TICKET NOT FOUND---")
            print(list_AllRedstorAccounts[counter_RedstorAccount]['AccountName'])
            print("'TIME ELAPSED:'", value_DaysFromLastBackup)
            print(list_AllRedstorAccounts[counter_RedstorAccount]['LastBackupMessage'])
            print("LAST BACKUP MESSAGE LENGTH: ", len(convertByChar(body_CreateTicket['subject'])))
            if check_UpdatedLBM == True:
                check_UpdatedLBM = False
                print("LAST BACKUP MESSAGE UPDATED")
            print("TICKET IS BEING CREATED...")
            time.sleep (10)
            request_CreateTicket = requests.post("https://desk.zoho.com/api/v1/tickets", data = json.dumps(body_CreateTicket), headers = headers) # send API request to zohodesk to create ticket with info found in body
            print("TICKET API REQUEST RESPONSE CODE:", request_CreateTicket)
            pprint.pprint(body_CreateTicket)
            print(" \n \n ")
            

        # if ticket update occurred
        if check_ExistingTicket == True: # if check was changed to true
            check_ExistingTicket = False # reset the check to false 
            
    
    
    counter_RedstorAccount += 1
print("COMPLETED WITH ERRORS/FAILED ACCOUNTS DETECTED:", counter_TotalBackupsDetected)
print("COMPLETED WITH ERRORS DETECTED: ", counter_TotalCompletedWithErrors)
print("OLD OR FAILED BACKUPS DETECTED: ", counter_TotalOldOrFailedBackups)
print("TOTAL EXISTING TICKETS", counter_CountTotalExistingTickets)
print("NEW TICKETS CREATED:", counter_CreatedTickets)
print("OLD/FAILED BACKUPS FOUND:")
pprint.pprint(list_OldOrFailedAccounts)
