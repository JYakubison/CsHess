# CsHess
A Slack Bot written in python that allows two users to play chess in a direct message.

Project was started as a way to learn Python and how to interact with a web api. 

Current version is a complete prototype and fully functional. 

Plans For Future Versions:
- Improved UI (Specifically Fixing Box Alignment)
- More (and more detailed) Notifications
- Option to play games in a thread
- Leaderboard/Win Count Tracking
- Improved Game Storage Organization

Typing "/challenge [@user]" will send out a challenge
![Capture 1](/Images/Capture1.PNG)

Upon accepting a challenge the challenged user will be given the option of which color to play
![Capture 2](/Images/Capture2.PNG)

Moves are then typed by both players into a group direct message in the form "m: a2a4"
The program accepts moves in the UCI move format
![Capture 3](/Images/Capture3.PNG)
![Capture 4](/Images/Capture4.PNG)
