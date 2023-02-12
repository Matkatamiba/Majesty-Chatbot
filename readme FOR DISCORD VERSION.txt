Go to C:\Users\yourname\Documents\My Games\MajestyHD\Mods
and make a new folder. Call it whatever and put all this in there.

Download Python 3. Feel free to read through the code in any of these files. Python and Majesty's custom .GPL (GamePlay Language) are both fairly easy to read and are a fun way to learn coding.


Since this won't be very broadly used, I'm not going to host a server for it like other discord bots do. It's easy enough to set up your own bot to run it when you need it (for the like 5 people this is relevant to). To set up a bot account on Discord, you will need to follow these steps:

- You can create a bot account by going to the Developer Dashboard (https://discord.com/developers/applications).

- Click on "Applications" in the left-hand menu, then click the blue "New Application" button on the top right.

- Call your bot whatever you want and accept the terms.

- On the left bar, select Bot. Click the blue Add Bot button on the right. (If it prompts you to save in any of these steps, save.)

- Check Message Content Intent (about halfway down the page)

- Press the blue Reset Token near the top of this page. It should give you a very long series of numbers and letters. Take this token and copy paste it into the token in the Discord-bot.py file near the top (currently, it's on line 8).

- On the left side, go to OAuth2. Check Bot and then check Read Message History. Go to URL Generator on the left side and check the same Bot and Read Message History.

- Copy the Generated URL into your browser and you should be able to invite your bot to join whatever servers you have invite powers for.

- Run the Discord-bot.bat file. This should install the needed modules for python and start the bot in your command window. You should see chat messages for servers you added it to in the chat window.

Open the Discord Bot.py file to view in your IDE and run the file with the play button. 
It'll ask you what channel you want to run it on and how often you want heroes to be custom named. 
Commands for Discord are: !create _____(creates a custom named hero), and !save. You'll need to type !save in Discord chat when you want to write to file and compile the game files. Reboot the game and the names should be there.


other files in the folder:
Gplbcc.exe compiler: This was put out by one of the Majesty Devs for modding purposes
GPL_COMPILER.bat file: This runs the Majesty compiler with and creates .bcd files
compiled.bcd: The compiled code for Majesty to read
TwitchHeroes.gplproj, TwitchHeroes.mmxml: Files for modding that point the mod on what to read