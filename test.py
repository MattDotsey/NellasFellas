from helpers import get_user_dict
from datetime import datetime
import time
import json
import requests
import sqlite3

connection = sqlite3.connect("sleepercal.db")
values = connection.execute("SELECT * FROM team_ktc_values").fetchall()
user_dict = get_user_dict()

column_names = [user_dict[ele]['team_name'] for ele in user_dict]

column_names[0:0] = ['id', 'date']

print(values)