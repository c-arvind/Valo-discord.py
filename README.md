# ValoGG
A Discord bot for Valorant that allows users to view various statistics of theirs and any discord user in their server without having to launch the game.

The endpoints for the API used in this project have been taken from [Henrik-3](https://github.com/Henrik-3/unofficial-valorant-api) so huge shoutout to him for somehow bypassing Riot's username-password system to access user data.

This bot is currently not hosted publicly as the API has a rate-limit and it isn't endorsed or legalized by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.

Feel free to clone or fork and use this code at your own discretion. Reach me out on discord (Cn0n#6790) if you find any of the endpoints to be deprecated or if you have any queries/feedback.

## Features
Simple user-game account linking
![link](https://user-images.githubusercontent.com/81007178/159135502-73d271e4-0067-4a0c-8b8d-bceea046b907.png)

Live match tracking
![live](https://user-images.githubusercontent.com/81007178/159135498-d164c6b5-72f7-4ade-8b24-922ba6d41952.png)

Match History Analysis
![history](https://user-images.githubusercontent.com/81007178/159135479-8da10aa9-1b19-4a26-ad15-81793d8bab1a.png)

User Statistics
![stats](https://user-images.githubusercontent.com/81007178/159135501-7545f4f6-f9e5-4a1c-871d-7e36193ccd56.png)

## Commands
```
v.link [username] [tag]
```
Links your ValorantID (name#tag) to your Discord ID (can be changed infinite times)
```
v.live <!@user_id>
```
Shows status of tagged user (self default) inside the game. Needs a friend request to be accepted initially to form connection
```
v.history <!@user_id>
```
Shows competitive history of tagged user (self default) as a graph for better visualization
```
v.stats <!@user_id>
```
Displays match statistics of tagged user (self default). Endpoint info derived from TRN API 

## Files
1. `api.py` contains functions to return parsed json data from api calls
2. `bot.py` has all the discord commands to interact with user
3. `database.py` connects bot with a mongodb database to map discord user with valorant ID
4. `graph.py` contains the plotting function for the history command

## Future Scope
Additional functions:
* Last played match details
* Realtime status of region
* slash commands instead of prefixed chat commands
* help command to assist user

This bot is a personal project for my own server but maybe in the future, if there is demand then I might deploy and scale the bot with cleaner code. All the code written in these .py files are 100% my own work so it would be appreciated if you could help me improve writing better python :)

