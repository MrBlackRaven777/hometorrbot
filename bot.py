import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import config
import utils
import os
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

upd = Updater(token=config.token)
dsp = upd.dispatcher



def path(bot, upd):
    utils.pickle_write(upd.message.chat_id, "is_expl_on", False)
    fav_list = list(utils.pickle_read(upd.message.chat_id,'favorites').keys())
    markup = telegram.ReplyKeyboardMarkup(
        utils.create_markup(fav_list, upd.message.chat_id), one_time_keyboard=True)
    bot.sendMessage(chat_id=upd.message.chat_id,
                    text="Choose folder from favorites, file system or cancel", reply_markup=markup, one_time_keyboard=True)

  
def echo(bot, upd):
    msg = upd.message.text
    ch_id = upd.message.chat_id
    favorites = utils.pickle_read(ch_id,'favorites')
    fav_list = list(favorites.keys())
    full_path = utils.pickle_read(ch_id, 'curr_dir')
#    print(full_path)
    dirs = next(os.walk(full_path))[1]
    if utils.pickle_read(ch_id,'is_expl_on') == True:
        if msg in dirs:
            print(2)
            utils.pickle_write(ch_id, "curr_dir", full_path + "\\" + msg)
            answer = utils.explorer(ch_id, msg)
            markup = telegram.ReplyKeyboardMarkup(
                    utils.create_markup(answer, ch_id))
            answer = None
        elif msg == "Done":
            answer = "Choosen folder: " +  utils.pickle_read(ch_id,'curr_dir')
            markup = telegram.ReplyKeyboardRemove()
        else:
            print(3)
            answer = "No directory named \"{0}\" in \"{1}\". Try again".format(msg, full_path)
            markup = telegram.ReplyKeyboardMarkup(utils.create_markup(dirs, ch_id))
        
        bot.sendMessage(chat_id=ch_id,
                        text=answer, reply_markup=markup)
    else:
        if msg == 'Choose folder':
            print(4)
            utils.pickle_write(ch_id, "is_expl_on", True)
            full_path = str(utils.pickle_read(ch_id,'favorites').get("Root"))
            print(full_path)
            utils.pickle_write(ch_id, "curr_dir", full_path)
            answer = utils.explorer(ch_id, "")
            markup = telegram.ReplyKeyboardMarkup(
                        utils.create_markup(answer, ch_id))
            answer = "Choose destination folder"
            
        elif msg in fav_list:
            print(1)
            utils.pickle_write(ch_id, "curr_dir", favorites.get(msg))
            answer = "Choosen folder: " + favorites.get(msg)
            markup = telegram.ReplyKeyboardMarkup(
                    utils.create_markup(fav_list, ch_id))
        else:
            answer = "Unknown command"
            markup = telegram.ReplyKeyboardRemove()
        bot.sendMessage(chat_id=ch_id,
                        text=answer, reply_markup=markup, one_time_keyboard=True)


def start(bot, upd):
#Starts bot, creates shelves for new user and setting up them with default folders for enviroment, where bot working
    new_user = True
    for d, dirs, files in os.walk(os.getcwd()):
        for f in files:   
            if str(upd.message.chat_id) in f:
                    new_user = False
    if new_user == True:
        favorites = utils.os_choose()
        curr_dir = favorites.pop("curr_dir")
        utils.pickle_write(upd.message.chat_id, "curr_dir", curr_dir)
        utils.pickle_write(upd.message.chat_id, "favorites", favorites)
        utils.pickle_write(upd.message.chat_id, "is_expl_on", False)
        reply_text = "Yours OS is: " + os.name + ". Your storage successfully created. Welcome!" 
    else:
        reply_text = "You're already my user. Send me /reset to destroy your personal settings"
    bot.sendMessage(chat_id=upd.message.chat_id, text=reply_text)


def reset(bot, upd):
    markup = telegram.ReplyKeyboardRemove()
    bot.sendMessage(chat_id=upd.message.chat_id, text=utils.pickle_remove(upd.message.chat_id), reply_markup=markup)    
    

def my_id(bot, upd):
    bot.sendMessage(chat_id=upd.message.chat_id, text= "Your id is: " + str(upd.message.chat_id))
    


path_handler = CommandHandler("path", path)
dsp.add_handler(path_handler)

start_handler = CommandHandler("start", start)
dsp.add_handler(start_handler)

reset_handler = CommandHandler("reset", reset)
dsp.add_handler(reset_handler)

echo_handler = MessageHandler(Filters.text, echo)
dsp.add_handler(echo_handler)

myid_handler = CommandHandler("myid", my_id)
dsp.add_handler(myid_handler)

upd.start_polling()
upd.idle()
