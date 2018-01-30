import config
import os
import sys
import pickle
import platform
import math
#from bot import is_expl_on as is_expl_on


def create_markup(button_list, is_expl_on, pg_num=1):
    button_list.sort()
    blen = len(button_list)
    keyboard = []
    boobs =  9 #not my fetish, just max number of Buttons On One Board Setting =) 
    # boobs should be a square of number max count columns and rows in cusfom reply keyboard.
    try:
        buttons_on_page_list = button_list[(pg_num-1)*boobs:min(pg_num*boobs, blen)]
        sqrb = int(math.sqrt(boobs))
        keyboard = [[buttons_on_page_list[x+y*sqrb] for x in range(min(sqrb, len(buttons_on_page_list)-y*sqrb))] 
                    for y in range(int(math.ceil(len(buttons_on_page_list)/sqrb)))]
        if is_expl_on == True:
            if pg_num==1 and blen>boobs:
                last_row = ["Back", "Done", "More -->"]
            elif len(button_list[(pg_num-1)*boobs:]) > boobs:
                last_row = ["Back", "<-- Less", "More -->"]
            elif len(button_list[(pg_num-1)*boobs:]) <= boobs and pg_num > 1:
                last_row = ["Back", "<-- Less"]
            elif pg_num == 1 and blen <= boobs:
                last_row = ["Back", "Done"]
        else:
            last_row = ['Choose folder', 'Cancel']
        keyboard.append(last_row)
        return keyboard
    except:
        return keyboard

def explorer(id, next_dir='', up=True):
#explore your filesystem, goes to the next_dir, up - is direction, where it goes in directory tree, 
#    where at the bottom is root directory, and at the top your folders
	curr_dir = pickle_read(id, 'curr_dir')
	if up == True:
		os.chdir(os.path.join(curr_dir, next_dir))
		dirs_list = get_dirs_list(os.getcwd())
		pickle_write(id, 'curr_dir', os.getcwd())
		msg=''
	else:
		prev_dir = os.path.split(curr_dir)[0]
		if os.path.exists(prev_dir):
			os.chdir(prev_dir)
			dirs_list = get_dirs_list(prev_dir)
			pickle_write(id, 'curr_dir', prev_dir)
			msg=''
		else:
			dirs_list=get_dirs_list(curr_dir)
			msg='there is no path ' + prev_dir
	return {'msg' : msg, 'dirs_list' : dirs_list}
			

def pickle_write(id, param_name, state):
    root_dir = os.getcwd()
    os.chdir(os.path.join(home_dir(), "users_storage"))
    name = 'pickle_{0}_{1}.txt'.format(id, param_name)
    try:    
        storage = open(name, 'wb')
        pickle.dump(state, storage)
        storage.close()
    except:
        print(sys.exc_info())
    os.chdir(root_dir)


def pickle_read(id, param_name):
    root_dir = os.getcwd()
    os.chdir(os.path.join(home_dir(), "users_storage"))
    name = 'pickle_{0}_{1}.txt'.format(id, param_name)
    try:    
        storage = open(name, 'rb')
        data = pickle.load(storage)
        storage.close()
    except:
        data = str(sys.exc_info())
    os.chdir(root_dir)
    return data
    
   
def pickle_remove(id):
    root_dir = os.getcwd()
    os.chdir(os.path.join(home_dir(), "users_storage"))
    try:
        for d, dirs, files in os.walk(os.getcwd()):
            for f in files:   
                if str(id) in f:
                        os.remove(f)
        msg = 'Succesfully removed'
    except:
        msg = sys.exc_info()
    os.chdir(root_dir)
    return msg


def get_dirs_list(path):
        dirs_list = []
        for f,d,fi in os.walk(path):
            dirs_list = d
            break
        return dirs_list

    
def os_choose():  
    if os.name == "nt":
        return {"curr_dir": os.path.expanduser("~\\Documents"), "Root": "C:\\", "Download": os.path.expanduser("~\\Downloads"), "Documents": os.path.expanduser("~\\Documents"), "Default folder": os.getcwd()}
    elif os.name == "posix":
    	#условие для распознавания системы на андройде, может ложно срабатывать на одноплатниках типа raspberry pi
        if 'arm' in platform.platform():
    	    root = '/storage/emulated/0'
    	    return {"curr_dir": os.getcwd(), "Root": root, "Download": root + "/Download", "Movies": root + "/Movies", "Default folder": os.getcwd()}
        else:
            return {"curr_dir": os.path.expanduser("~"), "Root": "/", "Download": os.path.expanduser("~/Download"), "Movies": os.path.expanduser("~/Movies"), "Default folder": os.getcwd()}
    else:
        return {"curr_dir": "/"}
    
    
def home_dir(directory=config.project_name, top=os.getcwd()):
#func for search project directory in tree from top to bottom, need for correct work of pickle
    found = False
    for root, dirs, files in os.walk(top):
        for name in dirs:
            if name == directory:
                found = True
                return root+os.path.sep+directory
    if found == False:
        new_top = os.path.split(top)[0]
        return home_dir(directory,new_top)