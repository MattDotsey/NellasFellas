import json
import requests

'''
FIRST GOAL: TRANSLATE A TRANSACTION INTO OWNERS, PLAYERS, AND PICKS
'''

# make a dictionary of roster_ids: {user_id: display_name} 

#pull roster ids from rosters page

roster_response = requests.get("https://api.sleeper.app/v1/league/924332039963328512/rosters")
rosters = json.loads(roster_response.text)

# pull user_id and display_name from users request
users_response = requests.get("https://api.sleeper.app/v1/league/924332039963328512/users")
users = json.loads(users_response.text)



# loop through rosters to get roster_id, owner_id, and team name
# loop through rosters to get roster_id, owner_id, and team name
def get_user_dict():
    user_dict = {}
    for roster in rosters:
        roster_id = roster['roster_id']
        user_id = roster['owner_id']
        
        # loop through users and find entry where user_id = user_id from rosters
        for user in users:
                if user['user_id'] == user_id:
                        display_name = user['display_name']
                        try:
                            team_name = user['metadata']['team_name']
                        except:
                            team_name = display_name
        
        user_dict[roster_id] = {'user_id': user_id, 'display_name': display_name, 'team_name': team_name}
    
    return user_dict

# need to take user_dict and put it into an sql table so we can upload it to github



# get roster numbers



# create another table for all transactions

'''
past league IDs:
2020: 558709483453202432
2021: 651542763904610304
2022: 785754223395704832
2023: 924332039963328512
the "get a specific league" call might automatically update with past leagues
'''
league_ids = [558709483453202432, 651542763904610304, 785754223395704832]

#handle past years

'''
# loop through leagues
for league in league_ids:


    #CURRENT PROBLEM: HOW DO I DETERMINE AMOUNT OF WEEKS IN A SEASON?



    # loop through weeks
    for week in weeks:

        # pull all transactions from specific week where type: trade
        transact_url = "https://api.sleeper.app/v1/league/" + str(league) + "/transactions/" + str(week)
        transact_response = requests.get()
        transactions = json.loads(transact_response.text)

        #loop through transactions
        for transaction in transactions:

            #if type == trade:
            if transaction['type'] == 'trade':
'''
                
# handle current year
                