# from helpers import lookup
import datetime
from flask import Flask
import json
import requests
import sqlite3

#configure application
# app = Flask(__name__)

'''
This program should be run daily, and should insert any new trades from the past day into the trades database
'''

# make a dictionary of roster_ids: {user_id: display_name} 
# pull roster ids from rosters page

roster_response = requests.get("https://api.sleeper.app/v1/league/924332039963328512/rosters")
rosters = json.loads(roster_response.text)

# pull user_id and display_name from users request
users_response = requests.get("https://api.sleeper.app/v1/league/924332039963328512/users")
users = json.loads(users_response.text)

#hopefully can use rosters to get right 
rosters_response = requests.get("https://api.sleeper.app/v1/league/924332039963328512/rosters")
rosters = json.loads(rosters_response.text)

user_dict = {}

# loop through rosters to get roster_id and owner_id
for roster in range(len(rosters)):
     roster_id = rosters[roster]['roster_id']
     user_id = rosters[roster]['owner_id']
     
     # loop through users and find entry where user_id = user_id from rosters
     for user in range(len(users)):
               if users[user]['user_id'] == user_id:
                    display_name = users[user]['display_name']
                    user_dict.update({roster_id: {user_id: display_name}})


connection = sqlite3.connect("sleepercal.db")
cursor = connection.cursor()

today = datetime.date.today()
 
'''
results seem to be different than what is shown on sleeper site, season type showing as "off".
need to figure out at what point that changes
'''

state_response = requests.get("https://api.sleeper.app/v1/state/nfl")
state = json.loads(state_response.text)

# MAKE A PROGRAM TO SAVE THE DATE THAT THIS PROGRAM IS RUN AND THE season_type changes from "off" to "on"
# SMALL DB WILL HOLD THE DATE AND THE SEASON_TYPE FOR THAT DATE

season_type = state['season_type']
week = state['week']

cursor.execute("INSERT INTO season_state (date, week, season_type) values(?, ?, ?)", (today, week, season_type))
connection.commit()

# request call for round 1 2022 season first result trey sermon 9/13/22, last result 1/10/22
# ROUND 1 IS START OF SEASON TO END OF WEEK 1, ROUND 0 IS AFTER END OF SEASON

# ADJUST TRANSACTIONS FOR CURRENT WEEK
# Will need to see when season_type changes and adjust accordingly
if season_type == 'off' and week == 0:
     transacts_week = 1
else:
     transacts_week = week

transacts_response = requests.get(f"https://api.sleeper.app/v1/league/924332039963328512/transactions/{transacts_week}")
transactions = json.loads(transacts_response.text)

'''
pull transactions and use other functions to insert readable data into SQL database
'''

# compare number of trades in league during current week to number of trades 

# filter transactions results to just trades:
trades = []

for transaction in transactions:
     if transaction['type'] == 'trade':
          trades.append(transaction)

# insert all data points into db (assets under specific roster column)
# this has to be flexible enough to accomdate owners of different lengths

#("INSERT INTO season_state (date, week, season_type) values(?, ?, ?)", (today, week, season_type))

transaction_id = 0
date = ""
year = 0
owners = []

# pick out important information from trade and assign players to new owners to be inserted into database
for trade in range(len(trades)):
    owners = trades[trade]['roster_ids']
    json_owners = json.dumps(owners)
    transaction_id = trades[trade]['transaction_id']
    date = today
    year = today.year
    str_converter = {1:"roster1_rec", 2:"roster2_rec", 3:"roster3_rec", 4:"roster4_rec", 5:"roster5_rec", 6:"roster6_rec", 7:"roster7_rec", 8:"roster8_rec", 9:"roster9_rec", 10:"roster10_rec", 11:"roster11_rec", 12:"roster12_rec"}
    # commented out for now, may not actually need this
    # roster1_rec = roster2_rec = roster3_rec = roster4_rec = roster5_rec = roster6_rec = roster7_rec = roster8_rec = roster9_rec = roster10_rec = roster11_rec = roster12_rec = []
    # tup_converter = {1:roster1_rec, 2:roster2_rec, 3:roster3_rec, 4:roster4_rec, 5:roster5_rec, 6:roster6_rec, 7:roster7_rec, 8:roster8_rec, 9:roster9_rec, 10:roster10_rec, 11:roster11_rec, 12:roster12_rec}
    query = f"INSERT INTO test_trans (transaction_id, date, season, owners" 
    params = [transaction_id, date, year, json_owners]

    # make a list of all assets going to each owner
    # add roster column for specific owners to INSERT statement 
    for owner in owners:
        # commented out roster lists, don't think i will need
        # need to reset roster_rec for each owner?
        # roster1_rec = roster2_rec = roster3_rec = roster4_rec = roster5_rec = roster6_rec = roster7_rec = roster8_rec = roster9_rec = roster10_rec = roster11_rec = roster12_rec = []
        # takes specific owner and sets id_str equal to string representation of roster_rec
        id_str = str_converter[owner]
        query += f", {id_str}"

        assets = []

        # if draft picks were traded
        if trades[trade]['draft_picks'] != []:
            draft_picks = trades[trade]['draft_picks']

            # loop through draft picks, and if owner_id == owners[owner], add pick to assets for that owner
            for draft_pick in range(len(draft_picks)):
                if draft_picks[draft_pick]['owner_id'] == owner:
                    assets.append(draft_picks[draft_pick])
          
        # if players were traded
        if trades[trade]['adds'] != None:
            adds = trades[trade]['adds']
               
            #add the players to proper list
            for add in adds:
                if adds.values()[add] == owners[owner]:
                    assets.append(adds.keys()[add])
        json_assets = json.dumps(assets)
        params.append(json_assets)
        
    # convert params from list to tuple
    params = tuple(params)

    # finish getting query to INSERT statement form
    query += ") values(?, ?, ?, ?" + (len(owners) * (", ?")) + ")"
    
    print(query)
    print(params)
    # insert trade into database
    cursor.execute(query, params)
    connection.commit()