import datetime
import os
from botoptions import BotOptions
from dboperations import DataBaseOperations
from bothandler import BotHandler

photoIdList = []

''' 
Project: Telegram Bot
Language: Python
Server: heroku

1. create a menu +
2. add menu functions +
3. add right version of registration (lets add 'sex' of person in database)+
4. i want to get description from photo+
5. add game method (instead hello func) +
6. create game logic 
7. add more users +
8. test test test

Need to do "TO DO" - 4
'''

def get_time():
    now = datetime.datetime.now()
    today = now.day
    hour = now.hour + 3
    minute = now.minute
    data = {"today": today, "hour": hour, "minute": minute}
    return data

def main():
    # DB operation
    db = DataBaseOperations(os.environ['DATABASE_URL'])
    # Bot api telegram
    greet_bot = BotHandler(os.getenv("TOKEN"))
    # Bot with my functions
    bot = BotOptions(greet_bot, db)
    new_offset = None
    while True:
        greet_bot.get_updates_json(new_offset)
        last_update = greet_bot.get_last_update()
        time = get_time()
        if(last_update):
            last_update_id = last_update['update_id']
            # If Update is MEASSAGE
            if (last_update.get('message')):
                if(last_update.get('message').get('text')):
                    # If message type is text ->
                    bot.say_something(last_update)
                elif (last_update.get('message').get('photo')):
                    # If message type is photo (file) ->
                    data = bot.get_photo_and_data(last_update)
                    if (data):
                        db.add_user(data)
                elif (last_update.get('message').get('voice')):
                    data = bot.recognize_audio(last_update)
                    print(data)
            # If update is CALLBACK
            if (last_update.get('callback_query')):
                if(last_update.get('callback_query').get('data')):
                    bot.menu_switcher(last_update)
            new_offset = last_update_id + 1
    cur.close()
    conn.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
