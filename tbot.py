import requests
import datetime
import random
import os
from time import sleep


class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates_json(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(self.api_url + method, data=params)
        print(response.json())
        result_resp = response.json()["result"]
        return result_resp

    def get_last_update(self):
        result = self.get_updates_json()

        if len(result)>0:
            last_update = result[-1]
        else:
            last_update = None
        return last_update

    def get_chat_id(update):
        chat_id = update['message']['chat']['id']
        return chat_id

    def send_message(self, chat, text):
        params = {'chat_id': chat, 'text':text}
        method = 'sendMessage'
        response = requests.post(self.api_url + method, data=params)
        return  response

    def send_photo(self, chat, file_id):
        params = {'chat_id':chat, 'photo': file_id}

    def send_photo(self, chat, photo):
        params = {'chat_id': chat, 'photo': photo}
        method = 'sendPhoto'
        response = requests.post(self.api_url + method, data=params)
        return response

greet_bot = BotHandler(os.getenv("TOKEN"))
hi_text = ("привет", "здравствуй", "ку", "hello", "hi", "q")
time_text = ("сколько время", "время", "дата", "date", "time")
photo_text = ("фото", "фотография", "photo", "next")
now = datetime.datetime.now()


def get_time():
    now = datetime.datetime.now()
    today = now.day
    hour = now.hour + 3
    minute = now.minute
    data = {"today":today, "hour":hour, "minute":minute}
    return data

def main():
    new_offset = None
    while True:
        greet_bot.get_updates_json(new_offset)
        photoIdList = []
        last_update = greet_bot.get_last_update()
        time = get_time()
        if(last_update):
            if(last_update['message'].get('text')):
                last_update_id = last_update['update_id']
                last_chat_text = last_update['message']['text']
                last_chat_id = last_update['message']['chat']['id']
                last_chat_name = last_update['message']['chat']['first_name']
                # Приветствие
                if last_chat_text.lower() in hi_text:
                    greet_bot.send_message(last_chat_id, "Привет, друг {}".format(last_chat_name))
                # Время
                if last_chat_text.lower() in time_text:
                    greet_bot.send_message(last_chat_id,
                                        "Сегодня {today}, время {hour}:{minute}"
                                           .format(today=time['today'], hour=time['hour'], minute=time['minute']))
                # Фото
                if last_chat_text.lower() in photo_text:
                    if(photoIdList):
                        greet_bot.send_photo(last_chat_id, random.choice(photoIdList))
            if(last_update.get('photo')):
                last_update_id = last_update['update_id']
                last_photo_id = last_update['photo']['file_id']
                photoIdList.append(last_photo_id)
                print(photoIdList)
            new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()