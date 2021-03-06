import random
from context import recognize
import cloudconvert

show_topics = ("/a")
show_text = ("/s ", "!s ")
topic_text = ("!t ", "/t ", "t  ", ".t ")
game_text = ("игра", "game", "играть", "play")
time_text = ("сколько время", "время", "дата", "date", "time")
reg_text = ("регистрация", "зарегестрироваться", "рег", "registration")
userdata = {'username': '', 'name': '', 'sex': '', 'photo': '', 'description':''}
users_list = [{}]

''' 
1) i can create list of userdata
add userdata with username and after it add next info about this user

or
2) i need asynk io 


now i will do first
'''

class BotOptions:
    def __init__(self, greet_bot, db):
        self.greet_bot = greet_bot
        self.database = db

    # And add try exept everywhere TO DO (2)
    # user[0] - username, user[1] - name, user[2] - sex, user[3] - photo, user[4] - desription
    def game(self, last_update, like = False):
        # If not registred -> send message about it!
        last_chat_id = last_update['callback_query']['message']['chat']['id']
        last_chat_username = last_update['callback_query']['message']['chat']['username']
        data = self.database.get_users()
        # TO DO set another sex (3)
        # TO DO to change it like -> t[t.index('b')] (4)
        if like:
            for user in data:
                if (user[0] == last_chat_username):
                    sex = user[2]
            # need to create algo that give people another people
            # -> FINISH THIS PART
            user = random.choice(data)
            if (not (user[2] == sex)) and (not(user[0] == last_chat_username)):
                self.greet_bot.send_user_photo(last_chat_id, user[3], user[4], user[1])
        else:
            self.greet_bot.send_message(last_chat_id, "Next photo")

        return data

    def recognize_audio(self, last_update):
        last_chat_audio = self.greet_bot.get_file_json(last_update['message']['voice']['file_id'])
        url = self.greet_bot.get_file(last_chat_audio['file_path'])
        api = cloudconvert.Api('VTodTciTcRpWfKqMgSCd32fMnXiih1G4P6i5gDl5WtXlUjgWBqV98GKLs2dg8CC4')
        process = api.createProcess({
            "inputformat": "ogg",
            "outputformat": "wav"
        })
        file = process.start({
            "input": "download",
            "file": url,
            "outputformat": "wav",
            "converteroptions": {
                "audio_bitrate": 128,
            },
            "save":True,
        })
        file = process.download('outputfile.ext')
        print(file)
        text = recognize(file)
        return text

    def get_photo_and_data(self, last_update):
        last_chat_name = last_update['message']['chat']['first_name']
        last_chat_username = last_update['message']['chat']['username']
        last_photo_id = last_update['message']['photo'][0]['file_id']
        last_photo_caption = last_update['message'].get('caption')
        for user in users_list:
            if (user.get('username')==last_chat_username):
                user['username'] = last_chat_username
                user['name'] = last_chat_name
                #user['sex'] -> in menu switcher
                user['photo'] = last_photo_id
                user['description'] = last_photo_caption
                return user
        return None

    def menu_switcher(self, last_update):
        # Here is switch callback (1: hello, 2: registratiom, 3:rules, 4:about us)
        userdata = {'username': '', 'name': '', 'sex': '', 'photo': '', 'description':''}
        keys = ('game', 'registration', 'rules', 'about', 'male', 'female', 'like', 'next')
        data = last_update['callback_query']['data']
        last_chat_id = last_update['callback_query']['message']['chat']['id']
        last_chat_name = last_update['callback_query']['message']['chat']['first_name']
        last_chat_username = last_update['callback_query']['message']['chat']['username']
        # This is bad TO DO (3)
        if (data == keys[0]):
            self.greet_bot.send_message(last_chat_id, "Hello {}, my friend. Let's play!".format(last_chat_name))
            self.game(last_update)
        elif (data == keys[1]):
            userdata['username'] = last_chat_username
            users_list.append(userdata)
            self.greet_bot.send_message_with_sex_buttons(last_chat_id, "Choose sex:")
        elif (data == keys[2]):
            self.greet_bot.send_message(last_chat_id, "Please don't spam to this bot. Thank you.".format(last_chat_name))
        elif (data == keys[3]):
            self.greet_bot.send_message(last_chat_id, "I am junior python developer. "
                                                      "Here is my application. You are welcome {}.".format(last_chat_name))
        elif (data == keys[4]):
            for user in users_list:
                if (user.get('username')==last_chat_username):
                    user['sex'] = keys[4]
            self.greet_bot.send_message(last_chat_id, "Send photo for profile in game "
                                                      "and add the caption(your description - briefly about yourself):")
        elif (data == keys[5]):
            for user in users_list:
                if (user.get('username')==last_chat_username):
                    user['sex'] = keys[5]
            self.greet_bot.send_message(last_chat_id, "Send photo for profile in game "
                                                      "and add the caption(your description - briefly about yourself):")
        elif (data == keys[6]):
            self.game(last_update, like=False)
        elif (data == keys[7]):
            self.game(last_update, like=True)
        print(data)

    def save_record(self, topic, last_chat_text):
        self.database.add_record(topic, last_chat_text)

    def get_records_by_topic(self, topic):
        records = self.database.get_records(topic)
        return records

    def get_topics(self):
        topics = self.database.get_topics()
        return topics

    def say_something(self, last_update):
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']
        # Type /a
        if (last_chat_text.lower()[0:2] in show_topics):
            records = self.get_topics()
            records = set(records)
            for message in records:
                self.greet_bot.send_message(last_chat_id, message)
        # Type /s
        if (last_chat_text.lower()[0:3] in show_text):
            topic = last_chat_text.lower()[3:]
            records = self.get_records_by_topic(topic)
            records = set(records)
            for message in records:
                self.greet_bot.send_message(last_chat_id, message)
        # Type /t
        if (last_chat_text.lower()[0:3] in topic_text):
            topic = last_chat_text.lower()[3:last_chat_text.lower().find('/r ')].replace('\n', '')
            message = last_chat_text.lower()[last_chat_text.lower().find('/r ')+3:]
            if message != '' and message is not None:
                self.save_record(topic, message)
                self.greet_bot.send_message(last_chat_id, "Record was added")
            topic = None
            message = None
        # Type "game"
        if last_chat_text.lower() in game_text:
            # Send buttons
            self.greet_bot.send_message_with_menu_buttons(last_chat_id, "Hello {}, make a choice:".format(last_chat_name))
        # Type "registration"
        if last_chat_text.lower() in reg_text:
            self.greet_bot.send_message_with_sex_butons(last_chat_id, "Choose sex:")
            self.greet_bot.send_message(last_chat_id, "And after it send photo")
            # Wait photo!
            # TO DO
        return last_update_id
