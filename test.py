from helpers import get_user_dict
from datetime import datetime
import time
import json
import requests
import sqlite3

connection = sqlite3.connect("sleepercal.db")
cursor = connection.cursor()
today = datetime.now().date()

ktc_dict = {'Plan = No plan': 173410, 'Breezy Bargain Hunters': 140742, 'Lowly Luca': 153312, 
             'Sod Was an Inside Job': 129761, 'Dynasty Wealth Management': 112887, 'T’s Dirty Dynasty': 110706, 
            'This Is Fun, Guys': 118258, 'JDSchirmann': 100321, 'The RyCU': 95720, 
            'Dear Leaders': 98780, 'Harambeerz': 101712, 'Cowboy Kev': 86120}

user_dict = {1: {'user_id': '342039644478783488', 'display_name': 'jsturi', 'team_name': 'Dynasty Wealth Management', 'value': 112962}, 
             2: {'user_id': '359101595713011712', 'display_name': 'tonzy74', 'team_name': 'T’s Dirty Dynasty', 'value': 110375}, 
             3: {'user_id': '741536030460678144', 'display_name': 'lbattis3', 'team_name': 'Lowly Luca', 'value': 152874}, 
             4: {'user_id': '346483781626253312', 'display_name': 'Dotsey', 'team_name': 'Sod Was an Inside Job', 'value': 129473}, 
             5: {'user_id': '736753480521355264', 'display_name': 'JDSchirmann', 'team_name': 'JDSchirmann', 'value': 99335}, 
             6: {'user_id': '558769193443491840', 'display_name': 'kbeldoch', 'team_name': 'Plan = No plan', 'value': 173532}, 
             7: {'user_id': '558779697058643968', 'display_name': 'cbiancaniello', 'team_name': 'Breezy Bargain Hunters', 'value': 140575}, 
             8: {'user_id': '559947017810345984', 'display_name': 'SzabiKiss', 'team_name': 'Dear Leaders', 'value': 100151}, 
             9: {'user_id': '476296883191410688', 'display_name': 'JakeMaggioncalda', 'team_name': 'This Is Fun, Guys', 'value': 119053}, 
             10: {'user_id': '560600692638785536', 'display_name': 'rrausch', 'team_name': 'The RyCU ', 'value': 96142}, 
             11: {'user_id': '560649734496948224', 'display_name': 'KevyKevs', 'team_name': 'Cowboy Kev', 'value': 86665}, 
             12: {'user_id': '560651431425011712', 'display_name': 'Harambeerz', 'team_name': 'Harambeerz', 'value': 101493}}

query = "INSERT INTO team_ktc_values (date, r1_value, r2_value, r3_value, r4_value, r5_value, r6_value, r7_value, r8_value, r9_value, r10_value, r11_value, r12_value) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
params = [today]

for owner in range(1, 13):
    params.append(user_dict[owner]['value']) 

params = tuple(params)

print(params)