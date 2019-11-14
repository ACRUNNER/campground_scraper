import requests
from checker import Checker
from random import random
import time
import credentials



def telegram_bot_sendtext(bot_message):
    
    bot_token = credentials.BOT_TOKEN
    bot_chatID = credentials.BOT_CHAT_ID
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
    
checker = Checker()

while True:

	result = checker.check_campsites()

	if result:
		print (result)
		test = telegram_bot_sendtext("Found a website! Campground: " + result[1] + " Date: " + result[0])
	else:
		print 'Found Nothing'
		test = telegram_bot_sendtext("Found Nothing")

	time.sleep(60 * 30 + 60 * 60 * random())

