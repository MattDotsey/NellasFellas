# from helpers import lookup
import datetime
from flask import Flask, session, render_template
from flask_session.__init__ import Session
import json
import requests
import sqlite3

from helpers import get_user_dict

today = datetime.date.today()

#configure application
app = Flask(__name__)

roster_response = requests.get("https://api.sleeper.app/v1/league/924332039963328512/rosters")
rosters = json.loads(roster_response.text)

# pull user_id and display_name from users request
users_response = requests.get("https://api.sleeper.app/v1/league/924332039963328512/users")
users = json.loads(users_response.text)

#hopefully can use rosters to get right 
rosters_response = requests.get("https://api.sleeper.app/v1/league/924332039963328512/rosters")
rosters = json.loads(rosters_response.text)
 
'''
results seem to be different than what is shown on sleeper site, season type showing as "off".
need to figure out at what point that changes
'''

state_response = requests.get("https://api.sleeper.app/v1/state/nfl")
state = json.loads(state_response.text)

# SAVE THE DATE THAT THIS PROGRAM IS RUN AND THE season_type changes from "off" to "on"
# SMALL TABLE WILL HOLD THE DATE AND THE SEASON_TYPE FOR THAT DATE

season_type = state['season_type']
week = state['week']

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

user_dict = get_user_dict()

def get_db_connection():
    conn = sqlite3.connect("sleepercal.db")
    # cursor = connection.cursor()
    return conn

@app.route('/')
def index():
    """home page"""
    "big ass table with display of all trades"
    conn = get_db_connection()
    trades = conn.execute("SELECT * FROM transactions").fetchall()
    
    trades = [list(ele) for ele in trades]
    
    '''
    go through each trade, 
    translate each draft pick into easy to understand terms, 
    translate each player into easy to understand terms.
    ''' 
    adds_counter = 0
    for trade in trades:
         
        # iterate through trades to find strings
        for item in range(5,17):
            # all assets converted from db to actual text stored here
            final_asset_list = []

            # since we should just be checking only assets received, 
            # should be able to just check whether or not it is None
            if trade[item] is not None:
                #set db_str_asset_list equal to all assets received in a trade
                db_str_asset_list = trade[item]   
                # change string version of text to an actual list of all assets 
                actual_asset_list = json.loads(db_str_asset_list)
                
                # iterate through all items in a specific asset list:
                for asset in actual_asset_list:    
                    
                    # if x, then it is a draft pick
                    if isinstance(asset, dict):    
                        for key in asset:
                            if key == 'season':
                                season = asset['season']
                                round = asset['round']
                                if round == 1:
                                    round = "1st"
                                elif round == 2:
                                    round = "2nd"
                                elif round == 3:
                                    round = "3rd"
                                elif round == 4:
                                    round = "4th"
                                elif round == 5:
                                    round = "5th"
                                
                                orig_owner = user_dict[actual_asset_list[0]['roster_id']]['team_name']
                                easy_read = f"{orig_owner}'s {season} {round}"
                                final_asset_list.append(easy_read)
                            
                    # if it's a list that means it's a player, 
                    # replace player_id with player name from player table
                    elif isinstance(asset, str):
                        player_name = list(conn.execute("SELECT player_name FROM players WHERE player_id = ?", (asset,)).fetchall())
                        player_name = list(player_name[0])
                        player_name = player_name[0]
                        final_asset_list.append(player_name) 
                trade[item] = final_asset_list                           

    conn.close()
    
    return render_template("index.html", user_dict = user_dict, trades = trades)

@app.route("/team_val_tracker")
def team_val_tracker():

    """This page will only contain a chart showing the values of each team over time"""
    
    conn = get_db_connection()
    trades = conn.execute("SELECT * FROM transactions").fetchall()
    
    trades = [list(ele) for ele in trades]


if __name__ == '__main__':
    app.run()
# have a separate page for each     