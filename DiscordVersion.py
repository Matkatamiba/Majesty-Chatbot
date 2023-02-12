import discord
import os
import subprocess

client = discord.Client()

# Make a discord bot and input your token here
token = 'put your token here'

usernames = set()
rarity = int(input("How often do you want custom-named heroes to spawn? (eg: 1 in 3) Enter the denominator: ")) -1
print ("Heroes will have custom names "+ str(100/(rarity+1))+ "% of the time")
print ("Connecting to Discord...")

# the file of the generated Majesty code
file_path = os.path.join(os.getcwd(), "HeroNamer.gpl")  # Use a relative file path


def is_alphanumeric_comma_space(string):
    for char in string:
        if not (char.isalnum() or char == "," or char == " "):
            return False
    return True


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


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Loop over all the text channels in the server
    for channel in message.guild.text_channels:
        print(f'{message.author} in {channel.name}: {message.content}')
        message = message.content
        valid_username = True

        if message.startswith("!create "):
            #check to make sure there's nothing but letters, numbers, commas, and spaces
            _, username = message.split("!create ")
            for char in username:
                if not is_alphanumeric_comma_space(char):
                    valid_username = False
                    break
            if valid_username:
                usernames.add(username)
                print("Added", username, "to hero list.")
                print("Current hero list:", usernames)
            else:
                print("Disallowed name: ", username)

        # writes hero names to file on typing !save
        if message.startswith("!save"):
            write_to_json_file(list(usernames), file_path)

            # Run the Majesty compiler after saving the names to the .gpl file
            subprocess.call(["GPL_COMPILER.bat"])

client.run(token)








