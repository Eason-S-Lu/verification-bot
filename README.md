# verification-bot
A verification bot for dicord<br>
The bot.py file is the bot.<br><br>

To run the bot you need Docker<br>
<h3>Instructaion to setup and run the bot</h3>
1. Complete the env.example and rename it to .env<br>
2. Modify ALLOWED_DOMAINS = ["pausd.us"] to a domain you want to allow, in line 15 of bot.py<br>
2. Use cd to the dir. where the bot.py file resides<br>
3. run <i>docker build -t verfication-bot .</i><br>
4. run <i>docker run --name bot -d verfication-bot</i><br>
5. to stop the program run <i>docker stop --signal SIGKILL bot</i><br>