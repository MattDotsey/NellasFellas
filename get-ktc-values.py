import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from os import path

'''
Not Finished, not usable at this time
'''

#get trade values from KTC website
#can optionally specify superflex/non-SF (sf by default)
#can optionally include draft pick values (included by default)
def getTradeValues(superflex=False, include_picks=True):
    url = 'https://keeptradecut.com/dynasty-rankings?filters=QB|WR|RB|TE'
    if include_picks:
        url = url + '|RDP'
    if not superflex:
        url = url + '&format=1'
    players = BeautifulSoup(get(url).text, features='lxml').select('div[id=rankings-page-rankings] > div')
    player_list = []
    for player in players:
        e = player.select('div[class=player-name] > p > a')[0]
        pid = e.get('href').split('/')[-1]
        name = e.text.strip()
        try:
            team = player.select('div[class=player-name] > p > span[class=player-team]')[0].text.strip()
        except:
            team = None
        position = player.select('p[class=position]')[0].text.strip()[:2]
        position = 'PICK' if position == 'PI' else position
        try:
            age = player.select('div[class=position-team] > p')[1].text.strip()[:2]
        except:
            age = None
        val = int(player.select('div[class=value]')[0].text.strip())
        val_colname = 'SF Value' if superflex else 'Non-SF Value'
        player_list.append({'PlayerID':pid,'Name':name,'Team':team,'Position':position,'Age':age,val_colname:val})
    return pd.DataFrame(player_list)

#combine dataframes with superflex/non-sf values into single dataframe
def combineTradeValues(sf_df, nonsf_df):
    merged_df = pd.merge(sf_df, nonsf_df, how='outer', on='PlayerID', suffixes=('_sf','_nonsf'))
    for col in ['Name','Team','Position','Age']:
        merged_df[col] = merged_df[col + '_sf'].fillna(merged_df[col + '_nonsf'])
    return merged_df[['PlayerID','Name','Team','Position','Age','SF Value','Non-SF Value']]

#get superflex and non-superflex values
# commented out superflex 
# sf_df = getTradeValues(superflex=True)
nonsf_df = getTradeValues(superflex=False)
#merge into single dataframe and export to csv

# commented out two lines because were going to put it in sql instead of csv
# merged_df = combineTradeValues(sf_df, nonsf_df)
# merged_df.to_csv(csv_path, index=False)

'''
At this point I need to figure out how I want to build the table and store this data
The overarching goal is going to be to take the KTC values from the dataframe and somehow combine
them with the trade information from the sql tables I already have. 

Potential issues: what if names do not match up perfectly? how can i spot this ahead of time, how can I prevent it?
What if two players have the same name? how can i sort through that?
What is the format of the table going to be? how can i store values of players over time when the players are also going to be changing?
'''

'''
Temporal Tables are the answer!!
'''