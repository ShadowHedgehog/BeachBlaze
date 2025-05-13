#!/bin/sh
echo "Beach Blaze Bot Setup"
echo "Press the approprite key to start an action"
echo "x) Close the setup.sh script"
echo "0) Information about Beach Blaze"
echo "1) Launch the Beach Blaze bots"
echo "2) Install required python packages"
echo "3) How to use guide"
while true; do
	read -n 1 -p "Enter Option: " option
	case $option in
		[x]* )
			echo
			echo "setup.sh is now closing"
			exit 1
		;;
		[0]* )
			echo
			echo "Beach Blaze"
			echo "Beach Blaze is a simple Giveaways and simple polls bot for Discord and Revolt.chat"
		;;
		[1]* )
			echo
			python main.py
		;;
		[2]* )
			echo
			echo "The setup is now installing the required python packages needed to use the Beach Blaze source code."
			sudo pip install discord.py
			sudo pip install discord
			sudo pip install git+https://github.com/EnokiUN/voltage
			sudo pip install python-dotenv
			sudo pip install requests
		;;
		[3]* )
			echo
			echo "The setup is now installing the required python packages needed to use the Beach Blaze source code."
			echo "Giveaway Setup: command and arguments are: <botprefix>giveaway time winners prize"
			echo "People can join the giveaways just by clicking on the :tada: emoji on the bot's message. Beach Blaze will NEVER ask you to verify to join a giveaway."
			echo "Poll Setup: command and arguments are: <botprefix>poll question answer1 answer2"
			echo
			echo "This section shows potiental scams that can occur related to giveaway bots like Beach Blaze that you should watch out for."
			echo "Phishing/Fake Sites:"
			echo "The only website Beach Blaze has is beachblaze.netlify.app and"
			echo "impersonator site can have malicious content in it like the Bookmark scam to execute malicious javascript code or a phishing login page both to steal your account information."
			echo "Fake Bots:"
			echo "People tend to create impersonator bots to do either Fake QR Verification scams to steal your account or"
			echo "make you Authorize an application that will join random (most likely scam) servers for you to join a giveaway."
			echo "Beach Blaze will NEVER ask you do do any of these things. To join a giveaway, you click on the :tada: reaction and you are in."
		;;
		*)
			echo
			echo "This is not a valid option"
		;;
	esac
done