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

# MAKE A PROGRAM TO SAVE THE DATE THAT THIS PROGRAM IS RUN AND THE season_type changes from "off" to "on"
# SMALL DB WILL HOLD THE DATE AND THE SEASON_TYPE FOR THAT DATE

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

# program to select all players a roster has recieved in a trade this year
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
    for trade in trades:
         
        # iterate through trades to find strings
        for item in range(len(trade)):
            check = trade[item]
               
            # if the string is a list in string format, and the first item in the string is a dict
            # it is a draft pick or a player
            if isinstance(check, str) and trade[item][0] == '[' and trade[item][1] == '{':
                # convert into actual list
                actual_list = json.loads(check)
                    
                # iterate through dictionaries in list
                for x in range(len(actual_list)):
                    # if it's a draft pick
                    if 'season' in actual_list[x]:
                        season = actual_list[x]['season']
                        round = actual_list[x]['round']
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
                        
                        orig_owner = user_dict[actual_list[x]['roster_id']]['name']
                        post_owner = user_dict[actual_list[x]['owner_id']]
                        easy_read = f"{orig_owner}'s {season} {round}"
                        trade[item] = easy_read
                         
                    # if it's a player
                    if 'adds' in actual_list[x]:
                        player_id = x['adds'].keys()
                        print(player_id)
                        # player = conn.execute("SELECT player_name FROM players WHERE player_id = ?", ).fetchall()


                    '''
                    STOPPING POINT

                    NEED TO FIGURE OUT HOW TO ACCESS PLAYER_ID IN 

                    {'adds': {'7547': 11}}
                    '''


                    




    print(trades) 
    conn.close()
    
    return render_template("index.html", user_dict = user_dict, trades = trades)

if __name__ == '__main__':
    app.run()
# have a separate page for each     