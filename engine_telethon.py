import configparser

from icecream import ic
from telethon.sync import TelegramClient, events
import telethon

# read config file
from telethon.tl.types import Message

config = configparser.ConfigParser()
config.read("config.ini")

# create 'constants'
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']
user_id = config['Telegram']['user_id']
client = TelegramClient(username, int(api_id), api_hash, )
stop = True
client.start()


def start_work():
    with client:
        @client.on(events.NewMessage())
        async def handler(event):
            global stop
            ic('new reaction exist')
            if isinstance(event, telethon.events.newmessage.NewMessage.Event):
                if event.message:
                    message = event.message

                    if isinstance(message, Message):
                        text = message.text
                        if message.text == 'stop':
                            stop = True
                        elif message.text == 'start':
                            stop = False
                        ic(stop)
                        if not stop:
                            await client.forward_messages('me', [message])

        @client.on(events.MessageEdited())
        async def edit_handler(event):
            global stop
            ic(stop)
            print('edit reaction exist')
            if isinstance(event, telethon.events.messageedited.MessageEdited.Event):
                if event.message:
                    message = event.message

                    if isinstance(message, Message):
                        text = message.text
                        if not stop:
                            await client.forward_messages('me', [message])
                            await client.send_message('me', '^ edited ^')

        client.run_until_disconnected()
