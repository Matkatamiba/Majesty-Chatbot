@echo off
cd /d %~dp0
pip install discord
python "DiscordVersion.py"
echo Either the script is done running or your token is invalid
pause