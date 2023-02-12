Go to C:\Users\yourname\Documents\My Games\MajestyHD\Mods
and make a new folder. Call it whatever and put all this in there.

Download Python 3. Feel free to read through the code in any of these files. Python and Majesty's custom .GPL (GamePlay Language) are both fairly easy to read and are a fun way to learn coding.


To set up a bot account on Twitch, you will need to follow these steps:
You can create a bot account by going to the Developer Dashboard (https://dev.twitch.tv/dashboard).
Click on "Applications" in the left-hand menu, then click the "Create New Application" button.

- Fill out the form with the required information, including the name of your bot, a brief description, and a redirect URI.

- Once you have created your application, click on the "Generate" button under the "Client ID" section to generate a unique client ID for your bot.

- Now, you will need to create an access token for your bot so that it can authenticate with the Twitch API. To do this, click on the "Generate" button under the "Secret" section.
You might need to use this (https://twitchapps.com/tmi/) link and use the OAth Token from there. Some combination of these should work.

- You should find a client ID and authorization token. Use that info in twitchmajesty.py on lines 7 and 8 for those values (in quotes as shown), and save the .py file.



Setup for this mod:
You'll need Python 3 and to install a couple packages with it. You install package with pip install whateverthepackageis or by using an IDE and installing there. I use PyCharm and don't know much about setup besides this. I'm kinda dumb and not sure how to get it working without an IDE. At the bottom, go to Terminal and type (as separate commands)
pip install os
pip install requests
pip install time
pip install websocket
I think some of these are already installed, but just checking.

If that isn't working, you should be able to add them in under File > Settings > Project: TwitchHeroes > Project Interpreter > + symbol > find them in the list.

Open the twitchmajesty.py file to view in your IDE and run the file with the play button. It'll ask you what channel you want to run it on and how often you want heroes to be custom named. Enter both of these in the run field in the Python IDE. Commands for Twitch chat are !join (creates their username), !create _____(creates a custom named hero), and !save. You'll need to type !save in Twitch chat when you want to write to file and compile the game files. Reboot the game and the names should be there.


other files in the folder:
Gplbcc.exe compiler: This was put out by one of the Majesty Devs for modding purposes
GPL_COMPILER.bat file: This runs the Majesty compiler with and creates .bcd files
compiled.bcd: The compiled code for Majesty to read
TwitchHeroes.gplproj, TwitchHeroes.mmxml: Files for modding that point the mod on what to read