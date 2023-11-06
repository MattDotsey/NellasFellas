'''
This program will use the Selenium Library 
to capture the total value of each team, and save that value
to a table on a monthly basis. 

In the future, it might be possible to split this 
into multiple different tables over time. 
'''

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import get_user_dict
from datetime import datetime
import json
import requests
import sqlite3


service = Service()
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://keeptradecut.com/dynasty/power-rankings/teams?leagueId=924332039963328512&platform=Sleeper#")

ktc_value_dict = {}

# iterate through list of teams
teams = driver.find_elements(By.CLASS_NAME, "pr-tms-team-wrap")    
for team in teams:
    team_element = team.find_element(By.CLASS_NAME, "pr-team-info-name")
    
    # get name of team
    team_name = team_element.get_attribute("innerText")
    
    # get id of team, to cover any changes to team names
    # team_id = 

    team_value = 0

    # iterate through team's players, add player values to team_value variable
    players = team.find_elements(By.CLASS_NAME, "pr-team-player")
    for player in players:
        # player_name for debugging purposes only
        player_name = player.find_element(By.CLASS_NAME, "team-player-name").text
        player_value = int(player.find_element(By.CLASS_NAME, "team-player-value").get_attribute("innerText"))
        team_value += player_value
    
    #add value of team to player dictionary with team name as key
    ktc_value_dict[team_name] = team_value

driver.quit()         

# have team names and values, have to combine them with the actual team ids
# so table doesn't get screwed up if somebody changes their name
owner_info_dict = get_user_dict()

# had to put in this check because Rausch put a space after his name and KTC didn't catch it. 
# this should be set up so it won't affect things if he changes his name in the future (unless he puts a space after his new name)
if ktc_value_dict.get('The RyCU') is not None:
    ktc_value_dict['The RyCU '] = ktc_value_dict.pop('The RyCU') 

for sleeper in owner_info_dict:
    for ktc in ktc_value_dict:
        if owner_info_dict[sleeper]['team_name'] == ktc:
            owner_info_dict[sleeper]['value'] = ktc_value_dict[ktc]
            break

print(owner_info_dict)

''' 
now need to insert roster_id, date, and value into a table
'''

connection = sqlite3.connect("sleepercal.db")
cursor = connection.cursor()
today = datetime.now().date()

# this loop will take the owner_info_dict and use it to create a query that will store the team's information.
"INSERT INTO team_ktc_values (date, r1_value, r2_value, r3_value, r4_value, r5_value, r6_value, r7_value, r8_value, r9_value, r10_value, r11_value, r12_value) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
params = [today]

params = [today]

for owner in range(1, 13):
    params.append(owner_info_dict[owner]['value']) 

params = tuple(params)


cursor.execute("INSERT INTO team_ktc_values (date_taken, r1_value, r2_value, r3_value, r4_value, r5_value, r6_value, r7_value, r8_value, r9_value, r10_value, r11_value, r12_value) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
connection.commit()

connection.close()

'''
{1: {'user_id': '342039644478783488', 'display_name': 'jsturi', 'team_name': 'Dynasty Wealth Management', 'value': 112962}, 

2: {'user_id': '359101595713011712', 'display_name': 'tonzy74', 'team_name': 'T’s Dirty Dynasty', 'value': 110375}, 
3: {'user_id': '741536030460678144', 'display_name': 'lbattis3', 'team_name': 'Lowly Luca', 'value': 152874}, 
4: {'user_id': '346483781626253312', 'display_name': 'Dotsey', 'team_name': 'Sod Was an Inside Job', 'value': 129473}, 
5: {'user_id': '736753480521355264', 'display_name': 'JDSchirmann', 'team_name': 'JDSchirmann', 'value': 99335}, 
6: {'user_id': '558769193443491840', 'display_name': 'kbeldoch', 'team_name': 'Plan = No plan', 'value': 173532}, 
7: {'user_id': '558779697058643968', 'display_name': 'cbiancaniello', 'team_name': 'Breezy Bargain Hunters', 'value': 140575}, 
8: {'user_id': '559947017810345984', 'display_name': 'SzabiKiss', 'team_name': 'Dear Leaders', 'value': 100151}, 
9: {'user_id': '476296883191410688', 'display_name': 'JakeMaggioncalda', 'team_name': 'This Is Fun, Guys', 'value': 119053}, 
10: {'user_id': '560600692638785536', 'display_name': 'rrausch', 'team_name': 'The RyCU '}, 
11: {'user_id': '560649734496948224', 'display_name': 'KevyKevs', 'team_name': 'Cowboy Kev', 'value': 86665}, 
12: {'user_id': '560651431425011712', 'display_name': 'Harambeerz', 'team_name': 'Harambeerz', 'value': 101493}}
'''