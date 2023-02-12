import os
import requests
import websocket
import subprocess

# Register your bot with Twitch and obtain a client ID and an OAuth token
client_id = 'put your clientID here'
# Called Client Secret or Token
oauth_token = "put your token here"

# Start listening for messages from the chat and writing them to a JSON file
file_path = os.path.join(os.getcwd(), "HeroNamer.gpl")  # Use a relative file path
data = []
usernames = set()  # Use a set to store the usernames

# Prompt the user for the name of the channel they want the bot to be active in
channel_name = input("Enter the name of the channel you want the bot to be active in: ")
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


# Authenticate your bot with Twitch and join the channel once the connection is established
def on_open(ws):
    ws.send(f"PASS oauth:{oauth_token}")
    ws.send(f"NICK MajestyChatbot")
    ws.send(f"JOIN #{channel_name}")
    print("Connection to Twitch chat is open.")  # Print a message when the connection is opened


# Handle the case where the connection is closed
def on_close(ws):
    print("Connection to Twitch chat is closed.")  # Print a message when the connection is closed
    write_to_json_file(list(usernames), file_path)


# Handle messages received from the chat
def on_message(ws, message):
    #print("Received a message from the chat:", message)  # Print each message received from the chat
    process_message(message)  # Process the message

# Process each message received from the chat

def is_alphanumeric_comma_space(string):
    for char in string:
        if not (char.isalnum() or char == "," or char == " "):
            return False
    return True

def process_message(message):
    # Extract the username and message that was typed by the user
    username = message.split(".tmi.twitch.tv PRIVMSG #")[0].split("@")[1]
    message = message.split(":")[2]
    print(username, message)

    #if they type !join, it uses their username
    if message.startswith("!join"):
        usernames.add(username.capitalize())  # Add the username to the set

    # if they type !create, it instead uses the words after the !create command
    if message.startswith("!create "):

        #fix up the message for annoying formatting
        _,username = message.split("!create ")
        username = username.strip("\r\n")
        valid_username = True

        #check to make sure there's nothing but letters, numbers, commas, and spaces
        for char in username:
            if not is_alphanumeric_comma_space(char):
                valid_username = False
                break
        if valid_username:
            usernames.add(username)
            print("Added", username, "to hero list.")
        else:
            print("Disallowed name: ",username)

    #if ONLY the channel name types !save, it'll write to file to be compiled
    elif message.startswith("!save"):
        write_to_json_file(list(usernames), file_path)
        print("Written names to HeroNamer.gpl, please recompile game and relaunch")
        # Run the Majesty compiler after saving the names to the .gpl file
        subprocess.call(["GPL_COMPILER.bat"])

    print(usernames)
    data.append({
        "message": message

    })


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
