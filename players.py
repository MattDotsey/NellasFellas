import json
import requests
import sqlite3

'''
goal is to go through players database and add all new players to database on once weekly
'''

connection = sqlite3.connect("sleepercal.db")
cursor = connection.cursor()

player_response = requests.get("https://api.sleeper.app/v1/players/nfl")
players = json.loads(player_response.text)

for player in players:
    id = players[player]['player_id']
    name = players[player]['first_name'] + " " + players[player]['last_name']
    cursor.execute("INSERT OR IGNORE INTO players (player_id, player_name) values(?, ?)", (id, name))
    connection.commit()
connection.close()

