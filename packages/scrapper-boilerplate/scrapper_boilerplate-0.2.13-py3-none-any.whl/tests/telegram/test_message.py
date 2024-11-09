import os
from dotenv import load_dotenv
from scrapper_boilerplate.telegram import TelegramBot

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
bot = TelegramBot(TOKEN, CHAT_ID)


def test_send_message():
    msg = 'Teste de envio de mensagem!'
    assert bot.send_message(msg)
        
    