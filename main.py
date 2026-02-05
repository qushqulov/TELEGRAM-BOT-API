import time
import requests
from config import TOKEN

class Bot:
    def __init__(self, token):
        self.BASE_URL = f"https://api.telegram.org/bot{token}"
        self.offset = 0

    def getMe(self) -> dict:
        get_me_url = f"{self.BASE_URL}/getMe"
        response = requests.get(get_me_url)
        if response.status_code == 200:
            return response.json()
        raise Exception("Xatolik bor !!!")

    def get_updates(self) -> list:
        get_updates_url = f"{self.BASE_URL}/getUpdates"
        params = {
            'offset': self.offset,
            'limit': 10
        }
        response = requests.get(get_updates_url, params=params)
        if response.status_code == 200:
            return response.json().get('result', [])
        else:
            print("Xato:", response.status_code, response.text)
            return []

    def send_message(self, chat_id, text):
        send_message_url = f'{self.BASE_URL}/sendMessage'
        params = {
            'chat_id': chat_id,
            'text': text
        }
        requests.get(send_message_url, params=params)

    def send_photo(self,chat_id,photo):
        send_photo_url = f'{self.BASE_URL}/sendPhoto'
        params = {
            'chat_id':chat_id,
            'photo':photo
        }
        requests.get(send_photo_url,params=params)
        

    def send_audio(self,chat_id,audio):
        send_audio_url = f'{self.BASE_URL}/sendAudio'
        params = {
            'chat_id':chat_id,
            'audio':audio
        }
        requests.get(send_audio_url,params=params)

    def send_voice(self, chat_id, voice_file_id):
        url = f"{self.BASE_URL}/sendVoice"
        params = {
        "chat_id": chat_id,
        "voice": voice_file_id
    }
        requests.get(url, params=params)
    
    def start_polling(self):
        while True:
            updates = self.get_updates()
            time.sleep(1)

            for update in updates:
                message = update.get('message')
                if message:
                    chat_id = message['chat']['id']
                    text = message.get('text')
                    if text:
                        self.send_message(chat_id, text)
                    photos = message.get('photo')
                    if photos:
                      file_id = photos[-1]['file_id']
                      self.send_photo(chat_id, file_id)
                    audio =message.get('audio')
                    if audio:
                        file_id = audio['file_id']
                        self.send_audio(chat_id,file_id)
                    voice = message.get('voice')
                    if voice:
                        file_id = voice['file_id']  
                        self.send_voice(chat_id, file_id)

                    self.offset = update['update_id'] + 1
     
bot = Bot(TOKEN)
bot.start_polling()