# NellasFellas Dynasty Fantasy Football Trade Database

This project is a website that makes API calls to the sleeper.com website, and arranges information from the website into a webpage, so other members of the league can access the most recent transactions. I felt as though the Sleeper website did not have an easy way to look at recent trades, and though it might be interesting to me and the rest of the league I am in to be able to access that information

At this point in time the entire project is uploaded here to Github Pages, but because the website is not static, hosting the website in its current form for free is beyond my programming capabilities. Despite that, I still  think that it is a good showcase of my python, sql, and HTML skills. 

## Overview

In a regular fantasy football league, multiple teams of owners build their own teams of NFL Skill position players (like Wide Receivers and Running Backs) and compete against other owners in their league to see who can score the most points. Points are scored when the players on their team accumulate stats, like making a reception, gaining yards, or scoring touchdowns.

A dynasty fantasy football league is very similar, except that unlike regular fantasy football, the teams roll over from year to year, so the main ways that you can get new players on your team is by drafting incoming rookies and trading with other teams. Because of this, trading is much more important than in regular fantasy football, and a bad trade can prevent your team from being competitive for multiple years in the future. 

In my dynasty league, the members like to go back, look at old trades, and talk about who "Won" or "Lost" the trade as a manner of bragging rights. In reality it's just a consolation prize for not winning the league, but it's still fun to do. I thought I would try and make a website that made it easier to track those trades, to foster more friendly competition among league members.

## The Actual Project

### Players 

Since we use the website Sleeper.com to host our league, the main way I got information for the website was by making API calls to Sleeper.com, and storing the information in SQL databases on my computer, where it would be easier to work with when I needed it again for the website. Unfortunately, when I made API calls to the website to pull all of the recent transactions in the league, all of the players are referenced by their player ID number instead of their actual names. The players.py page makes an API call to the Sleeper website for a list of all of the players currently active in the NFL and their corresponding Sleeper player ID number, and stores all of them in a sqlite table. I chose to store them in a database because the API documentation asked that I only make calls to players once a day because of the size of the call.

### Transactions

In this section, I got all of the pertinent information about each specific trade from the league website and assembled them together into one table, so it would be easy to call them and list them on the new website. I again made API calls to the sleeper website to assemble a list of all of the owners in the league, a list of all the transactions in the league, and some other important information needed to make the transactions call. 

The transactions list from the API call contains a list of all transactions in the league, such as waiver claims and other less important information, so the program picks the trades out from the rest of the transactions, and appends each trade as its own element in a list. From there, the program iterates through each trade in the list and identifies the date the transaction took place, the unique transaction ID (Set as unique in the database structure to make sure there are no duplicates in the transactions table), the season the trade took place, the owners involved in the trade, and the assets (draft picks and players) involved in the trade. The program than takes all that information and uses string concatenation to build sql commands that eventually insert all of the information into a transactions table. 

<img src="docs/NellasFellas Transactions Table.png" alt="TransactTable" width="1250" height="350"/>

The biggest difficulty I had with this section was the fact that while most trades in our league involve 2 owners, there is theoretically the option for a trade to occur between any number of owners. Because of that, the table (and the rudimentary HTML front end) needed to be able to handle the edge cases of a 3, 4 or even 12 person trade. 

### Flask Framework and HTML Front End

In the final section of the project, I used Flask to combine the tables that I had built and present the information in a webpage. The final product is not actually a very large amount of code, but took a very long time for me to put together and required me to learn a lot more about JSON, SQL, and Python than I already did. 

<img src="docs/Webpage View.png" alt="TransactTable" width="1250" height="700"/>

This program basically does the same thing as the transactions program, but with a different start and end point. It takes the information from the transactions database, translates the different storage methods for players and draft picks into plain english, and then assembles them into lists that the HTML and Bootstrap can present to the user. 

### Team Power Rankings

The first project that I wanted to add on to the website is the ability to track total team value over time. I chose this project because it would be a good way to build a base of data that I might be able to analyze in future projects, while not being as large of an undertaking as some of the other ideas that I had. 

The issues that I encountered along the way shaped how I made the project, So the easiest way to explain how I worked through the project would be by explaining the problems that I had to solve. The first problem that I had was the issue of how I wanted to store the data. Originally my plan was to create a table that would store the values of individual players over time, and then I would pull current rosters for each team using the Sleeper API, and match players with their current values. That plan was very complicated for what I was trying to accomplish, and several problems popped up. The most annoying one was how to handle players with identical names. There wasn't an easy way to use the players table I already created and combine it with data scraped from the KeepTradeCut.com website while assigning the player value to the correct player when multiple players with the same name existed. I had a few different ideas for how to handle it (incorporating team or position into the players table, for instance) but instead of struggling through that, I decided to just scale back my ambitions a little bit, so I could get the table up and storing data for me as quickly as possible. 

My next plan was to just use the BeautifulSoup Library to scrape rosters and player values both from the KTC website, using a power rankings feature found on the website. The problem with this was when I found out that BeautifulSoup does not work on dynamically created HTML content, so I was not able to use it to scrape the information i wanted to. At this point I could either go back to my original plan, or learn the Selenium library, which seemed to offer the functionality I was looking for. I decided to try Selenium.



### Future Improvements

There are a couple different things I would add to or change about the website, given the chance.

1. Addition - The most interesting thing I would like to add to my website is to use a website (like KeepTradeCut.com) that logs individual player/draft pick values to keep track of the value of trades or teams over time. Something like a chart with a different line for each team showing how the team's value has changed over time, or clicking on a trade to open up a chart that shows the value of the trade in the time since the trade was made. The chart would be the easiest place to start, but the value of each trade over time would be the most difficult database design challenge I would have taken to this point. Both of those things would be a lot easier if I had a script that ran different programs at scheduled intervals, so I wouldn't always have to go back and run the programs myself. 

2. Change - The biggest change I would make would be to enchance the HTML of the website. Right now it's incredibly basic, but I would challenge myself to make it look a little nicer, if nothing else. I'm not looking for a career in web design, but I think i can do a little better than it is now. Beyond that, I would redesign the trade table so that each row would only contain the owners that were actually involved in the trade, instead of keeping it static like it is now. I think that would be a pretty sizable undertaking, though. A more simple change that I would be able to do with the knowledge I currently possess would be to take the chunk of code that I use to translate the less readable player_id and transaction dictionaries.
