import telegram
import asyncio
from scrapper_boilerplate.warnings import disable_warnings

disable_warnings()


class TelegramBot:
    """
    Telegram message handler
    - to get chat: access @getidsbot and type start to get id
    - to access token, create bot in @botFather and paste the token
    """ 

    def __init__(self, auth_token:str, chat_id:str):
        print('> iniciando módulo do telegram!')
        self.TOKEN = auth_token
        self.CHAT_ID = chat_id
        self.bot = telegram.Bot(token=self.TOKEN)

    async def _send_message(self, msg):
        try:
            print('> Enviando mensagem...')
            await self.bot.sendMessage(chat_id=int(self.CHAT_ID), text=msg)
            print('> Mensagem enviada com sucesso!')
            return True

        except Exception as error:
            print(f'> [ERRO] ao enviar mensagem! {error} ')
            return False

    async def _send_file(self, filename):
        """
        send a file to telegram
        """
        try:
            document = open(filename, 'rb')
            await self.bot.send_document(int(self.CHAT_ID), document)
            print('> Arquivo enviado com sucesso!')
            return True

        except Exception as error:
            print(f'> [ERRO] ao enviar arquivo! {error} ')
            return

    def send_message(self, msg):
        return asyncio.run(self._send_message(msg))
    
    def send_file(self, filename):
        return asyncio.run(self._send_file(filename))
