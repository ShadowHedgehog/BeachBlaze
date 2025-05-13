# Beach Blaze Bot Source Code

> [!NOTE]
> NOTICE: THIS SOURCE CODE IS DISCONTINUED! IF YOU WISH TO USE THIS, YOU ARE ON YOUR OWN! THIS REPO WILL NOT BE UPDATED THAT MUCH. I RECOMMEND USING [THE FUNTIME CHICA SOURCE CODE](https://codeberg.org/agentorangelarfleeze/FuntimeChica)

Beach Blaze is a simple Giveaways and Polls bot in one single bot. The bot has been created by the same people who made Shadow's Dark Network and SHADOW OS.EXE/Windows 11 Horror Edition

There was gonna be a Guilded bot but this has been cancelled.

## Requirements:

- Python 3.10 or newer
- 512mb disk and 512mb ram with a decent CPU (I don't recommend using a CPU that is like 30 years old)

## Setup

You are expected to have some knowledge with Python.

Step 1: Open the .env.example file and fill in everything it asks for.
- DISCORDBOTTOKEN= Put your Discord bot token here. (head over to discord.com/developers and create a new application, then head over to the bot tab and enable the message content intent. To get your token, click "reset token" and you will get your new bot token.)
- REVOLTBOTTOKEN= Put your Revolt.chat bot token here. (click "Create a Bot" and give it a name. You will see a token once you create your bot)
- DISCORDBOTPREFIX= Put the prefix you want the Discord bot to respond to here. (Default is $)
- REVOLTBOTPREFIX= Put the prefix you want the Revolt bot to respond to here. (Default is $)
- MODE= Put in the launch mode number.

MODE Numbers

- 0 = Discord and Revolt.chat bot
- 1 = Discord bot only
- 2 = Revolt.chat bot only

Step 2: After you setup the .env.example file, rename the file to .env

Step 3: After that, install the packages within the requirements.txt file

Step 4: Run the bot by using python main.py and enjoy.

## Changelog

May 13th, 2025

- Source code gets discontinued
- Uses .env file for easier setup.
- Discord bot now has a serverinfo, numberguessing, and rps command
- New setup.sh file that will help you setup the bot and run it and it includes information about the bot.
- Added a main.py file which includes launch modes

December 21st, 2023

- Added giveaways, serverinfo, rps, and numberguessing in the Revolt.chat bot

November 7th, 2023
- Discord bot has: Giveaways, a 2 answer poll system, and say commands
- Revolt bot has a 2 answer poll system and say commands
- Bot is licensed under the MIT license.