# -*- coding: utf-8 -*-
import math
import os
import utils
import config
import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

#upd = Updater(token=config.token)
#dsp = upd.dispatcher
#msg_id = 0
#
#def echo(bot, upd):
#    global msg_id
#    if msg_id == 0:
#        msg_id = bot.sendMessage(chat_id=upd.message.chat_id,
#                        text="first message").message_id
#        print(msg_id)
#
#    else:
##        bot.Message.edit_text(chat_id=upd.message.chat_id,
##                        text='You said: ' + upd.message.text, message_id = msg_id)
#        bot.edit_message_text(chat_id=upd.message.chat_id,
#                        text='You said: ' + upd.message.text, message_id = msg_id)
#        
#echo_handler = MessageHandler(Filters.text, echo)
#dsp.add_handler(echo_handler)
#
#upd.start_polling()
#upd.idle()        

#print(utils.pickle_read(332761, 'favorites').get('Documents'))
    
#print(utils.create_markup([],332761))
#print(glob(os.getcwd()+"\\*"))

#print(os.getcwd())
#os.chdir(utils.home_dir() + os.path.sep + "users_storage")
#print(os.getcwd())

#print(utils.home_dir())
#print(os.path.join(utils.home_dir(), "users_storage"))