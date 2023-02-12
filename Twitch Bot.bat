@echo off
cd /d %~dp0
pip install websocket-client
python "TwitchVersion.py"
echo Either the script is done running or your token is invalid
pause