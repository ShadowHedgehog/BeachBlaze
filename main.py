from dotenv import load_dotenv
import os
load_dotenv()
MODE = os.getenv("MODE")

if MODE == 0:
    os.system('python ./main-discord.py & python ./main-revolt.py')
    print("Starting: Beach Blaze Discord and Revolt.chat bot")
elif MODE == 1:
    os.system('python ./main-discord.py')
    print("Starting: Beach Blaze Discord bot")
elif MODE == 2:
    os.system('python ./main-revolt.py')
    print("Starting: Beach Blaze Revolt.chat bot")
else:
    print("MODE in the .env file is not using a valid option. Refer to the available options below:")
    print("0 = Discord and Revolt.chat bot")
    print("1 = Discord bot only")
    print("2 = Revolt bot only")
