# NellasFellas Dynasty Fantasy Football Trade Database

This project is a website that makes API calls to the sleeper.com website, and arranges information from the website into a webpage, so other members of the league can access the most recent transactions. I felt as though the Sleeper website did not have an easy way to look at recent trades, and though it might be interesting to me and the rest of the league I am in to be able toa ccess that information

At this point in time the entire project is uploaded here to Github Pages, but because the website is not static, hosting the website in its current form for free is beyond my programming capabilities. Despite that, I still  think that it is a good showcase of my python, sql, and HTML skills. 

## Overview

In a regular fantasy football league, multiple teams of owners build their own teams of NFL Skill position players (like Wide Receivers and Running Backs) and compete against other owners in their league to see who can score the most points. Points are scored when the players on their team accumulate stats, like making a reception, gaining yards, or scoring touchdowns.

A dynasty fantasy football league is very similar, except that unlike regular fantasy football, the teams roll over from year to year, so the main ways that you can get new players on your team is by drafting incoming rookies and trading with other teams. Because of this, trading is much more important than in regular fantasy football, and a bad trade can prevent your team from being competitive for multiple years in the future. 

In my dynasty league, the members like to go back, look at old trades, and talk about who "Won" or "Lost" the trade as a manner of bragging rights. In reality it's just a consolation prize for not winning the league, but it's still fun to do. I thought I would try and make a website that made it easier to track those trades, to foster more friendly competition among league members.

## The Actual Project

### Players 

Since we use the website Sleeper.com to host our league, the main way I got information for the website was by making API calls to Sleeper.com, and storing the information in SQL databases on my computer, where it would be easier to work with when I needed it again for the website. Unfortunately, when I made API calls to the website to pull all of the recent transactions in the league, all of the players are referenced by their player ID number instead of their actual names. The players.py page makes an API call to the Sleeper website for a list of all of the players currently active in the NFL and their corresponding Sleeper player ID number, and stores all of them in a sqlite database. I chose to store them in a database because the API documentation asked that I only make calls to players once a day because of the size of the call.

### Transactions

This was the most important part of the project, where I took all the different pieces that go into a specific trade, and assembled them together into one table, so it would be easy to call them and list them on 
