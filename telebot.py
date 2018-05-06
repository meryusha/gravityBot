import telepot
import sys
import time
from telepot.loop import MessageLoop
from firebase import firebase
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

#from firebase_admin import credentials


mfirebase = firebase.FirebaseApplication('https://gravitel-d0c7e.firebaseio.com', None)
#{'first_name': 'Your Bot', 'username': 'YourBot', 'id': 123456789}
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    textButtonOne = "Ranking"
    textButtonTwo = "Choosing a program"
    textButtonThree = "Find a person"
    textButtonFour = "UNI info"

    rankingOne = "By country"
    rankingTwo = "By major"
    rankingThree = "General"

    level = ["Graduate", "Undergraduate"]
    fund = ["Self-financed", "Scholarship"]
    location = ["Kazakhstan", "Abroad"]

    mainMenu = 'Main menu'

    rankingbuttons = [
        "1-50", "51-100", "101-150",
        "151-200", "201-251", "251-300",
        "301-350", "351-400", "401-450",
        "451-500", "501-550", "550-600"]

    main_markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=textButtonOne)], [KeyboardButton(text=textButtonTwo)],
            [KeyboardButton(text=textButtonThree), KeyboardButton(text=textButtonFour)]
        ]
    )

    unis = mfirebase.get('unis/', None)
    #uni = None
    #countrues = generateCountries(unis);
    #print(type(unis))
    if content_type == 'text':
        if mfirebase.get('users/' + str(msg['from']['id']) + "/findPerson", None):
            mfirebase.put('users/' + str(msg['from']['id']), name="findPerson", data=False, params={'print': 'pretty'})
            people = mfirebase.get('people/', None)

            message = ""
            if len(msg['text']) < 3:
                message = "Query is too short. Try again"
            else:
                for key in people.keys():
                     if msg['text'].lower() in key:
                        message += "People at " + key + ":\n\n"
                        for name in people[key].keys():
                            person = people[key][name]
                            message += "Name: " + name + ". Email: " + person['email'] + ". Admitted: " + str(person['admitted'])
                            message += ". Level: " + person['level'] + ". Major: " + person['major']
                            message += ". Telegram username: " + person['telegram'] + "\n\n"
            if len(message) == 0:
                message = "No such university found"
            bot.sendMessage(chat_id, message, reply_markup=main_markup)
        elif mfirebase.get('users/' + str(msg['from']['id']) + "/findUni", None):
            mfirebase.put('users/' + str(msg['from']['id']), name="findUni", data=False, params={'print': 'pretty'})
            message = ""
            if len(msg['text']) < 3:
                message = "Query is too short. Try again"
            else:
                for i in range(1, len(unis)):
                    if msg['text'].lower() in unis[i]['university_name'].lower():
                        message += unis[i]['university_name'] + "\n"
                        message += "Rank: " + str(unis[i]['world_rank']) +"\n"+ "Citations: " + str(unis[i]['citations']) +"\n"+ "Country: " + unis[i]['country'] + "\n\n"
            if len(message) == 0:
                message = "No such university found"
            bot.sendMessage(chat_id, message, reply_markup=main_markup)
        elif mfirebase.get('users/' + str(msg['from']['id']) + "/findCountry", None):
            mfirebase.put('users/' + str(msg['from']['id']), name="findCountry", data=False, params={'print': 'pretty'})
            l = generateCountries(unis, msg['text'])
            messageC = "Top 30 universities in " + msg['text'] + "\n\n"
            for i in range (1, len(l)):
                messageC += l[i] + "\n"
            if (len(l)==0):
                messageC = "No universities found"
            print(messageC)
            bot.sendMessage(chat_id, messageC, reply_markup=main_markup)
        elif msg['text'] == mainMenu:
            bot.sendMessage(chat_id, mainMenu, reply_markup=main_markup)
        elif msg['text'] == textButtonOne:
            bot.sendMessage(chat_id, 'University Ranking',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text=rankingOne)], [KeyboardButton(text=rankingTwo)], [KeyboardButton(text=rankingThree)], [KeyboardButton(text=mainMenu)]
                                ]
                            ))
        elif msg['text'] == textButtonTwo:
            bot.sendMessage(chat_id, textButtonTwo,
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text=level[0])], [KeyboardButton(text=level[1])], [KeyboardButton(text=mainMenu)]
                                ]
                            ))
        elif msg['text'] == textButtonThree:
            bot.sendMessage(chat_id, "Please enter a university name", reply_markup=ReplyKeyboardRemove())
            mfirebase.put('users/' + str(msg['from']['id']), name="findPerson", data=True, params={'print': 'pretty'})
        elif msg['text'] in level:
            mfirebase.put('users/' + str(msg['from']['id']), name="level", data=msg['text'], params={'print': 'pretty'})
            bot.sendMessage(chat_id, msg['text'],
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text=fund[0])], [KeyboardButton(text=fund[1])], [KeyboardButton(text=mainMenu)]
                                ]
                            ))
        elif msg['text'] in fund:
            mfirebase.put('users/' + str(msg['from']['id']), name="fund", data=msg['text'], params={'print': 'pretty'})
            bot.sendMessage(chat_id, msg['text'],
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text=location[0])], [KeyboardButton(text=location[1])], [KeyboardButton(text=mainMenu)]
                                ]
                            ))
        elif msg['text'] in location:
            mfirebase.put('users/' + str(msg['from']['id']), name="location", data=msg['text'], params={'print': 'pretty'})
            bot.sendMessage(chat_id, msg['text'],
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[[KeyboardButton(text=mainMenu)]
                                ]
                            ))
        elif msg['text'] == rankingThree:
            bot.sendMessage(chat_id, 'General Ranking',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text=rankingbuttons[0]), KeyboardButton(text=rankingbuttons[1]), KeyboardButton(text=rankingbuttons[2])],
                                    [KeyboardButton(text=rankingbuttons[3]), KeyboardButton(text=rankingbuttons[4]), KeyboardButton(text=rankingbuttons[5])],
                                    [KeyboardButton(text=rankingbuttons[6]), KeyboardButton(text=rankingbuttons[7]), KeyboardButton(text=rankingbuttons[6])],
                                    [KeyboardButton(text=rankingbuttons[9]), KeyboardButton(text=rankingbuttons[10]), KeyboardButton(text=mainMenu)]
                                ]
                            ))
        elif msg['text'] in rankingbuttons:
            myMsg = msg['text']
            message = "General rankings. Places " + myMsg + "\n\n"
            data = mfirebase.get('unis/', None)
            split = myMsg.split('-')
            for i in range(int(split[0]), int(split[1])+1):
                message += str(data[i]['world_rank']) + ") " + data[i]['university_name'] + "\n"
            print(message)
            bot.sendMessage(chat_id, message)

        # elif msg['text'] == textButtonFour:
        #     bot.sendMessage(chat_id, "Please enter a university name", reply_markup=ReplyKeyboardRemove())
        #     mfirebase.put('users/' + str(msg['from']['id']), name="findUni", data=True, params={'print': 'pretty'})
        elif msg['text'] == textButtonFour:
            bot.sendMessage(chat_id, 'Please enter a university name', reply_markup=ReplyKeyboardRemove())
            mfirebase.put('users/' + str(msg['from']['id']), name="findUni", data=True, params={'print': 'pretty'})
        #elif uni is not None:
            #bot.sendMessage(chat_id, unis['university_name'] + )
        elif msg['text'] == rankingOne:
            bot.sendMessage(chat_id, 'Please enter a country name', reply_markup=ReplyKeyboardRemove())
            mfirebase.put('users/' + str(msg['from']['id']), name="findCountry", data=True, params={'print': 'pretty'})
        # elif 'uni=' in msg['text']:
        # elif msg['text'] == textButtonThree:
        #     data = mfirebase.get('people/', None)
        #     message = "Database for people: "
        #     print(len(data))
        #     for key, value in data.items():
        #         #print (key)
        #         message = message + str(key) + "\n\n" + str(value)
        #     bot.sendMessage(chat_id, message)




def generateCountries(unis, country):
    print(country)
    #print(unis[1])
    list_uni = []
    for i in range(1, len(unis)):
        #print(unis[i] + i)
        if country.lower() in unis[i]['country'].lower():
            list_uni.append(str(unis[i]['world_rank']) + ") " + unis[i]['university_name'])
            if len(list_uni) > 30:
                return list_uni
    return list_uni


def findUni(unis, uni):
    uniInfo = ""
    for i in range(1,  len(unis)):
        #print(unis[i] + i)
        if unis[i]['university_name'] == uni:
            return  "rank: " + str(unis[i]['world_rank']) +"\n\n"+ "citations: " + str(unis[i]['citations']) +"\n\n"+  "country: " + unis[i]['country']
    return uniInfo


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