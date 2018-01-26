import os
import shelve
import sys
import pickle
import platform
import math
#from config import favorites as fav


def create_markup(button_list, sh_id, pg_num=1):
    blen = len(button_list)
    keyboard = []
    boobs =  9 #not my fetish, just max number of Buttons On One Board Setting =) 
    # boobs should be a square of number max count columns and rows in cusfom reply keyboard.
    buttons_on_page_list = button_list[(pg_num-1)*boobs:min(pg_num*boobs, blen)]
    sqrb = int(math.sqrt(boobs))
    keyboard = [[buttons_on_page_list[x+y*sqrb] for x in range(min(sqrb, 				len(buttons_on_page_list)-y*sqrb))] for y in range(int(math.ceil(len(buttons_on_page_list)/sqrb)))]
    if pickle_read(sh_id, "is_expl_on") == True:
        keyboard.append(["Back", "Done", "More"])
    else:
        keyboard.append(['Choose folder', 'Cancel'])
    return keyboard



def explorer_old(id, next_dir):
    curr_dir = pickle_read(id, "curr_dir")
    if next_dir != "":
        next_dir = "\\" + next_dir
    if curr_dir is None:
        return "No path"
    else:
        
        full_path = curr_dir + next_dir
        print(full_path)
        try:
            dirs_list = next(os.walk(full_path))[1]
            print(dirs_list)
            return dirs_list
        except:
            print(sys.exc_info())
            dirs_list = next(os.walk(curr_dir))[1]
            return dirs_list
            
def explorer(id, next_dir):
	#todo rewrite explorer with os.chdir())
	curr_dir = pickle_read(id, "curr_dir")
	try:
		os.chdir(next_dir)
		dirs_list = next(os.walk(os.getcwd()))[1]
		msg = ''
		pickle_write(id, 'curr_dir', os.getcwd())
	except:
		dirs_list = next(os.walk(curr_dir))[1]
		msg = sys.exc_info()
	return {'msg' : msg, 'dirs_list' : dirs_list}
    

def pickle_write(id, param_name, state):
    root_dir = os.getcwd()
    os.chdir("users_storage")
    name = 'pickle_{0}_{1}.txt'.format(id, param_name)
    #print("Going to write in {3}\\{0} value: {1} : {2}".format(name, param_name, state, os.getcwd()))
    try:    
        storage = open(name, 'wb')
        pickle.dump(state, storage)
        storage.close()
    except:
        print(sys.exc_info())
    os.chdir(root_dir)


def pickle_read(id, param_name):
    root_dir = os.getcwd()
    os.chdir("users_storage")
    name = 'pickle_{0}_{1}.txt'.format(id, param_name)
    try:    
        storage = open(name, 'rb')
        data = pickle.load(storage)
        storage.close()
        
    except:
        print(sys.exc_info())
    os.chdir(root_dir)
    return data
    
   
def pickle_remove(id):
    root_dir = os.getcwd()
    os.chdir("users_storage")
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

    
def os_choose():  
    if os.name == "nt":
        return {"curr_dir": os.path.expanduser("~"), "Root": "C:/", "Download": os.path.expanduser("~\\Downloads"), "Video": os.path.expanduser("~\\Videos"), "Default folder": os.getcwd()}
    elif os.name == "posix":
    	#условие для распознавания системы на андройде, может ложно срабатывать на одноплатниках типа raspberry pi
        if 'arm' in platform.platform():
    	    root = '/storage/emulated/0'
    	    return {"curr_dir": os.getcwd(), "Root": root, "Download": root + "/Download", "Movies": root + "/Movies", "Default folder": os.getcwd()}
        else:
            return {"curr_dir": os.path.expanduser("~"), "Root": "/", "Download": os.path.expanduser("~/Download"), "Movies": os.path.expanduser("~/Movies"), "Default folder": os.getcwd()}
    else:
        return {"curr_dir": "/"}
    
#pickle_write(332761, 'Root', 'C:\\')
#print(pickle_read(332761,'favorites'))
