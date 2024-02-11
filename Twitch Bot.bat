@echo off
cd /d %~dp0
python "TwitchMajesty.py"
echo Connection to Twitch closed. You may need to regenerate a token at https://twitchapps.com/tmi/ Rerun .bat file. 
pause