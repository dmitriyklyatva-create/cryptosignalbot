import requests
class TelegramNotifier:
    def __init__(self, token, chat_id):
        self.token = token; self.chat_id = chat_id
        self.url = f"https://api.telegram.org/bot{token}/sendMessage"
    def send_signal(self, data):
        msg = f"Signal: {data['signal']}\nConf: {data['confidence']}%"
        try: requests.post(self.url, json={'chat_id': self.chat_id, 'text': msg}); return True
        except: return False
