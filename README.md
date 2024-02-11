Twitch chat can rename heroes in game with chat commands. Twitch channel doesn't even have to be live!

!join		(adds their username to the hero list)
!name _____ 	(adds a custom named hero to the list, can be turned off)
!remove _____   (remove a name you don't like)

Mod files get downloaded to C:\SteamLibrary\steamapps\workshop\content\73230\2908092423 or your equivalent.

1. Create an Oauth token. Use the following link: https://twitchapps.com/tmi/ to get the OAuth Token for the next step. It looks something like oauth:li8efebxigsupoit6d84291onbem8e

2. In the OAuth.py file, replace the oauth_token value with the new oauth token in the quotes. Save the OAuth.py file.

3. Download Python 3 and install it. https://www.python.org/downloads/release/python-3121/ but any version of Python 3 should work.

4. Run the Twitch Bot.bat file.

5. A command prompt will open and you will be prompted to enter the channel you want to run it on, whether you want chat to custom name heroes (enter at thine own risk with Twitch chat), and how often you want heroes to be custom named.

6. People can now start naming stuff. List will be updated on the next level you start. Rerun the Twitch Bot.bat file if you want a full new set of names.

Try booting the game before starting the script so that Steam Workshop doesn't overwrite your mod files.
Names will be updated on hero spawn, so you'll see different names during their creation bars.

If you have issues, message the mod page or add me and I'll try to help.
Many thanks to Enerril for help coding the last jank part for Majesty. This should work with other mods, so long as they don't mess with the hero_birth function.
