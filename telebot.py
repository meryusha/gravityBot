import telepot
import sys
import time
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton



#{'first_name': 'Your Bot', 'username': 'YourBot', 'id': 123456789}
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    
    if content_type == 'text':
        if msg['text'] == '/key':
            bot.sendMessage(chat_id, 'testing custom keyboard',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text="Ilyuha kakashka"), KeyboardButton(text="Ilyuha kozyavka")]
                                ]
                            ))

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Got it')


bot = telepot.Bot('512216973:AAH8Rn3ZrBwWDx-q23nhWbDYUJVlRcbYT2o')
#print(bot.getMe())
#bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)