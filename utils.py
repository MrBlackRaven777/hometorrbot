import config
import os
import shelve
import sys
import pickle
import platform
import math
import glob
#from config import favorites as fav
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
Y  = '\033[33m' # yellow
B  = '\033[34m' # blue

def create_markup(button_list, sh_id, pg_num=1):
    blen = len(button_list)
    keyboard = []
    boobs =  9 #not my fetish, just max number of Buttons On One Board Setting =) 
    # boobs should be a square of number max count columns and rows in cusfom reply keyboard.
    print(G+'Create markup started'+W)
    try:
        buttons_on_page_list = button_list[(pg_num-1)*boobs:min(pg_num*boobs, blen)]
        print(G+'BOPL: ' + B+str(buttons_on_page_list)+W)
        sqrb = int(math.sqrt(boobs))
        keyboard = [[buttons_on_page_list[x+y*sqrb] for x in range(min(sqrb, len(buttons_on_page_list)-y*sqrb))] 
                    for y in range(int(math.ceil(len(buttons_on_page_list)/sqrb)))]
        if pickle_read(sh_id, "is_expl_on") == True:
            keyboard.append(["Back", "Done", "More"])
        else:
            keyboard.append(['Choose folder', 'Cancel'])
        print(G+'Create markup: '+ B+str(keyboard)+W)
        return keyboard
    except:
        print(G+'Create markup error: '+ B+str(sys.exc_info())+W)
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
    print(G+'Explorer: get values: '+B+str(id)+'   '+next_dir+W)
	#todo rewrite explorer with os.chdir())
    curr_dir = pickle_read(id, "curr_dir")
    print(G+'Explorer : curr_dir = ' + B+ curr_dir+ W)
    root_dir = os.getcwd()
    print(G+'Explorer : root_dir = ' + B+ root_dir+ W)
    next_dir = curr_dir + config.divider + next_dir
    print(G+'Explorer : next_dir = ' + B+ next_dir+ W)
    dirs_list=[]
    try:
#        os.chdir(curr_dir)
#        print(G+'Explorer : changed dir to ' + B+ os.getcwd()+ W)
        os.chdir(next_dir)
        print(G+'Explorer : changed dir to ' + B+ os.getcwd()+ W)
        dirs_list = get_dirs_list(os.getcwd())
        print(G+'Explorer : get dirs list: ' + B+ str(dirs_list)+ W)
        msg = ''
        pickle_write(id, 'curr_dir', os.getcwd())
    except FileNotFoundError:
        dirs_list = get_dirs_list(curr_dir)
        print(G+'Explorer : FNF error, get prev dirs list: ' + B+ str(dirs_list)+ W)
        msg = "No directory named \"%s\" in %s" % (next_dir, curr_dir)
    except:
        print(G+'Explorer: caught an unexpected error, see in msg'+W)
        dirs_list = get_dirs_list(curr_dir)
        msg = sys.exc_info()
#        for a,b,c in msg:
#            for d in c:
#                print(G+'Explorer Error: ' + R + d + W)
    os.chdir(root_dir)
    print(G+'Explorer: change dir to ' + B+ os.getcwd()+ W)
    print(G+'Explorer: Going to return: '+B+str({'msg' : msg, 'dirs_list' : dirs_list})+W)
    return {'msg' : msg, 'dirs_list' : dirs_list}
    

def pickle_write(id, param_name, state):
    root_dir = os.getcwd()
    os.chdir(os.path.join(home_dir(), "users_storage"))
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
    os.chdir(os.path.join(home_dir(), "users_storage"))
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
        print(G+'Get Dirs List: going to return: '+B+str(dirs_list)+W)
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
    
def home_dir(direct=config.project_name, top=os.getcwd()):
    found = False
    for root, dirs, files in os.walk(top):
        for name in dirs:
            if name == direct:
#                print("Found folder " + direct + " in " + root)
                found = True
                return root+os.path.sep+direct
    if found == False:
        new_top = os.path.split(top)[0]
#        print("Try to search in "+new_top)
        return home_dir(direct,new_top)

    
    
#pickle_write(332761, 'curr_dir', 'C:\\Users\\d.voskresenskiy\\Documents')
#print(pickle_read(332761,'favorites'))
#print(home_dir())