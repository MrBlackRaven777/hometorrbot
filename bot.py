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

#want to colorise  error messages in console output for better debug; synatax: print(R+"some red text"+W)
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
Y  = '\033[33m' # yellow
B  = '\033[34m' # blue



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

    if utils.pickle_read(ch_id,'is_expl_on') == True:    
        curr_dir = utils.pickle_read(ch_id, 'curr_dir')
        print(G+'Current directory is: ' + B + curr_dir+W)
        dirs_list = utils.get_dirs_list(curr_dir)
        print(G+'Directories here: '+B+str(dirs_list)+W)
        print(G+'Try to walk into directory ' + B + msg +W)
        if msg in dirs_list:
            print(2)
            expl_data = utils.explorer(ch_id, msg)
            answer = expl_data.get('msg')
#            print(expl_data.get('dirs_list'))
            markup = telegram.ReplyKeyboardMarkup(expl_data.get('dirs_list'))
        elif msg == "Done":
            answer = "Choosen folder: " +  utils.pickle_read(ch_id,'curr_dir')
            markup = telegram.ReplyKeyboardRemove()
        else:
            print(3)
            answer = "No directory named \"%s\" in \"%s\". Try again" % (msg, curr_dir)
            markup = telegram.ReplyKeyboardMarkup(utils.create_markup(dirs_list, ch_id))
        
        bot.sendMessage(chat_id=ch_id,
                        text=answer, reply_markup=markup)
    else:
        favorites = utils.pickle_read(ch_id,'favorites')
        fav_list = list(favorites.keys())
        if msg == 'Choose folder':
            print(G+'Echo: choose folder'+W)
            utils.pickle_write(ch_id, "is_expl_on", True)
            curr_dir = str(utils.pickle_read(ch_id,'favorites').get("Documents"))
            print(B + curr_dir + W)
            utils.pickle_write(ch_id, "curr_dir", curr_dir)
            answer = utils.explorer(ch_id, "").get('dirs_list')
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
#Starts bot, creates pickles for new user and setting up them with default folders for bot working enviroment
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
    start(bot, upd)
    

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
