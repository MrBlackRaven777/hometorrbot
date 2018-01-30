import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import config
import utils
import os
import logging
import time


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

upd = Updater(token=config.token)
dsp = upd.dispatcher


msg_id = 0
kb_page = 1
is_expl_on = False

def path(bot, upd):
    global is_expl_on 
    is_expl_on = False
    fav_list = list(utils.pickle_read(upd.message.chat_id,'favorites').keys())
    markup = telegram.ReplyKeyboardMarkup(
        utils.create_markup(fav_list, is_expl_on), one_time_keyboard=True)
    bot.sendMessage(chat_id=upd.message.chat_id,
                    text="Choose folder from favorites, file system or cancel", reply_markup=markup, one_time_keyboard=True)

  
def echo(bot, upd):
    msg = upd.message.text
    ch_id = upd.message.chat_id
    global msg_id 
    global kb_page
    global is_expl_on
    if is_expl_on == True:    
        curr_dir = utils.pickle_read(ch_id, 'curr_dir')
        dirs_list = utils.get_dirs_list(curr_dir)
        if msg in dirs_list:
            kb_page = 1
            expl_data = utils.explorer(ch_id, msg)
            answer = "Choose destination folder. Current folder is: " + utils.pickle_read(ch_id, 'curr_dir')
            markup = telegram.ReplyKeyboardMarkup(utils.create_markup(expl_data.get('dirs_list'), is_expl_on))
        elif msg == "Done":
            kb_page = 1
            answer = "Choosen folder: " +  utils.pickle_read(ch_id,'curr_dir')
            is_expl_on = False
            utils.pickle_write(ch_id, 'curr_dir', utils.pickle_read(ch_id, 'favorites').get('Root'))
            markup = telegram.ReplyKeyboardRemove()
        elif msg == "Back":
            kb_page = 1
            expl_data = utils.explorer(ch_id, up=False)
            answer = "Choosen folder: " +  utils.pickle_read(ch_id,'curr_dir')
            markup = telegram.ReplyKeyboardMarkup(utils.create_markup(expl_data.get('dirs_list'), is_expl_on))
        elif msg == "More -->":
            kb_page+=1
            answer = "Choosen folder: " +  utils.pickle_read(ch_id, 'curr_dir')
            markup = telegram.ReplyKeyboardMarkup(utils.create_markup(utils.get_dirs_list(curr_dir), is_expl_on, pg_num=kb_page))
        elif msg == "<-- Less":
            kb_page-=1
            answer = "Choosen folder: " +  utils.pickle_read(ch_id, 'curr_dir')
            markup = telegram.ReplyKeyboardMarkup(utils.create_markup(utils.get_dirs_list(curr_dir), is_expl_on, pg_num=kb_page))
        else:
            kb_page = 1
            answer = "No directory named \"%s\" in \"%s\". Try again" % (msg, curr_dir)
            markup = telegram.ReplyKeyboardMarkup(utils.create_markup(dirs_list, is_expl_on))
        
        bot.delete_message(chat_id=ch_id, message_id = msg_id)
        time.sleep(0.2) #needs to fix kb, when old custom kb removing, default kb layovers and if in this time switch on custom kb, it will underlays default kb and both of them hiding down
        #фикс для клавиатуры, когда удаляется сообщение, то старая клава убирается, вместо нее автоматом появляется обычная клава, если в этот момент придет новая кастомная, то она просто подсунется под стандартную, поэтому делаем задержку, чтоб инициализировалась стандарная, и поверх нее даем новую кастомную
        msg_id = bot.sendMessage(chat_id=ch_id, text=answer, reply_markup=markup).message_id
    else:
        favorites = utils.pickle_read(ch_id,'favorites')
        fav_list = list(favorites.keys())
        if msg == 'Choose folder':
            is_expl_on = True
            curr_dir = str(utils.pickle_read(ch_id,'curr_dir'))
            answer = utils.explorer(ch_id, "").get('dirs_list')
            markup = telegram.ReplyKeyboardMarkup(
                        utils.create_markup(answer, is_expl_on))
            answer = "Choose destination folder. Current folder is: " + curr_dir
            
        elif msg in fav_list:
            utils.pickle_write(ch_id, "curr_dir", favorites.get(msg))
            answer = "Choosen folder: " + favorites.get(msg)
            markup = telegram.ReplyKeyboardMarkup(
                    utils.create_markup(fav_list, is_expl_on))
        else:
            answer = "Unknown command"
            markup = telegram.ReplyKeyboardRemove()
        
        msg_id = bot.sendMessage(chat_id=ch_id, reply_markup=markup,
                        text=answer, one_time_keyboard=True).message_id


def start(bot, upd):
    global is_expl_on
#Starts bot, creates pickles for new user and setting up them with default folders for bot working enviroment
    new_user = True
    for d, dirs, files in os.walk(utils.home_dir()):
        for f in files:   
            if str(upd.message.chat_id) in f:
                    new_user = False
    if new_user == True:
        favorites = utils.os_choose()
        curr_dir = favorites.pop("curr_dir")
        utils.pickle_write(upd.message.chat_id, "curr_dir", curr_dir)
        utils.pickle_write(upd.message.chat_id, "favorites", favorites)
        is_expl_on = False
        reply_text = "Yours OS is: " + os.name + ". Your storage successfully created. Welcome!" 
    else:
        reply_text = "You're already my user. Send me /reset to destroy your personal settings"
    bot.sendMessage(chat_id=upd.message.chat_id, text=reply_text)


def reset(bot, upd):
    markup = telegram.ReplyKeyboardRemove()
    bot.sendMessage(chat_id=upd.message.chat_id, text=utils.pickle_remove(upd.message.chat_id), reply_markup=markup)    
    start(bot, upd)
    
    
def all(bot,upd):
#    print(telegram.message.MessageEntity.ALL_TYPES)
#    print(upd.message.entity(type))
    answer = r'''\ncode example\n'''
    bot.sendMessage(chat_id=upd.message.chat_id, text = answer)

path_handler = CommandHandler("path", path)
dsp.add_handler(path_handler)

start_handler = CommandHandler("start", start)
dsp.add_handler(start_handler)

reset_handler = CommandHandler("reset", reset)
dsp.add_handler(reset_handler)

#echo_handler = MessageHandler(Filters.text, echo)
#dsp.add_handler(echo_handler)

all_handler = MessageHandler(Filters.all, all)
dsp.add_handler(all_handler)

upd.start_polling()
upd.idle()
