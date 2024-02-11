import os
import websocket
import subprocess
from OAuth import oauth_token  # Import the variables from the config file

# Start listening for messages from the chat and writing them to a JSON file
file_path = os.path.join(os.getcwd(), "HeroNamer.gpl")  # Use a relative file path
data = []
usernames = set()  # Use a set to store the usernames

# Prompt the user for the name of the channel they want the bot to be active in
channel_name = input("Enter the name of the channel you want the bot to be active in: ")
# Prompt the user for allowing the use of !name
allow_name_command = input("Do you want to allow the use of !name for custom hero names? (yes/no): ").lower()
allow_name = allow_name_command == 'yes'
if allow_name:
    print("Users can use !name to specify custom hero names.")
else:
    print("Users cannot use !name to specify custom hero names.")
rarity = int(input("How often do you want custom-named heroes to spawn? (eg: 1 in 3) Enter the denominator: ")) -1
print ("Heroes will have custom names "+ str(100/(rarity+1))+ "% of the time")

# Connect to the Twitch chat using a websocket connection
ws = websocket.WebSocketApp("wss://irc-ws.chat.twitch.tv")


# formats the text file for Majesty so it transfers the names over and runs as code properly over there
def write_to_json_file(data, file_path):
    """Write the data to a GPL file at the specified file path.

    Args:
        data: A list of dictionaries containing the data to be written to the JSON file.
        file_path: The file path to the JSON file.
    """
    with open(file_path, "w") as f:
        # Write the additional text to the file
        f.write(
"""function HeroNamer(agent thisagent)
declare
    integer i, HeroCount;
    string name;
    list NameOptions;
    agent AIRootAgent;
begin
    AIRootAgent = $retrieveagent("GPLAIRoot");
    if ($HasAttribute("CustomNames", AIRootAgent) == False)
        begin\n""")

        for username in data:
            f.write('            NameOptions << "{}"'.format(username)+";\n")
        f.write(
f"""            $AddAttribute(AIRootAgent,"HeroNames","List",NameOptions);
        end
    $AddAttribute(AIRootAgent,"CustomNames","Boolean",True);
    HeroCount = $listsize(AIRootAgent's "HeroNames");
    if (HeroCount > 0)
        begin
            if ($randomnumber({rarity}) == 0)
                begin
                    i = $randomnumber(HeroCount) + 1;
                    name = $listmember(AIRootAgent's "HeroNames",i);
                    AIRootAgent's "HeroNames" -= name;
                    $SpecifyName(thisagent, name);
                end
        end
end""")


if oauth_token.startswith('oauth:'):
    oauth_token = oauth_token[len('oauth:'):]

# Authenticate your bot with Twitch and join the channel once the connection is established
def on_open(ws):
    ws.send(f"PASS oauth:{oauth_token}")
    ws.send(f"NICK MajestyChatbot")
    ws.send(f"JOIN #{channel_name}")
    print("Connection to Twitch chat is open.")


# Handle the case where the connection is closed
def on_close(ws, close_status_code, close_msg):
    print("Connection to Twitch chat is closed.")
    print("If you believe this is in error, recheck your token and enter it again.")
    write_to_json_file(list(usernames), file_path)


# Handle messages received from the chat
def on_message(ws, message):
    process_message(message)


def filter_alphanumeric_comma_space(string):
    allowed_chars = [char for char in string if (char.isalnum() and char.isascii()) or char == "," or char == " "]
    return ''.join(allowed_chars)


def process_message(message):
    # Extract the username and message that was typed by the user
    username = message.split(".tmi.twitch.tv PRIVMSG #")[0].split("@")[1]
    message = message.split(":")[2]
    print(username,":", message)

    # if they type !join, it uses their username
    if message.startswith("!join"):
        usernames.add(username.capitalize())  # Add the username to the set
        print("Added", username, "to hero list.")

    # if they type !name, it instead uses the words after the !name command, only works if !name is enabled
    elif allow_name and message.startswith("!name "):
        _,username = message.split("!name ")

        # removing nonenglish and sus symbols for security and functionality with Majesty GPL
        username = filter_alphanumeric_comma_space(username)
        usernames.add(username)
        print("Added", username, "to hero list.")

    # If they type !remove, it removes the specified username
    elif message.startswith("!remove "):
        _, username = message.split("!remove ")

        username = filter_alphanumeric_comma_space(username)
        if username in usernames:
            print("Removed", username, "from hero list.")
        else:
            print("Username not found:", username)
        usernames.discard(username)

    print("Current list of usernames:")
    for username in usernames:
        print(username)


    if message.startswith("!"):
        write_to_json_file(list(usernames), file_path)
        # Run the Majesty compiler after saving the names to the .gpl file
        try:
            subprocess.run(["GPL_COMPILER.bat"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Error running GPL_COMPILER.bat: {e}")


# Set the event handler for messages received from the chat
ws.on_message = process_message


# Set the event handlers for the websocket connection
ws.on_open = on_open
ws.on_close = on_close
ws.on_message = on_message

try:
    # Start the websocket connection and listen for messages from the chat
    ws.run_forever()


except websocket.WebSocketConnectionClosedException as e:
    print(f"Connection to Twitch chat was closed: {e}")
except websocket.WebSocketException as e:
    print(f"An error occurred with the websocket connection: {e}")
