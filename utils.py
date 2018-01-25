import os
import shelve
import sys
import pickle
import platform
#from config import favorites as fav


def create_markup(button_list, sh_id, num=1):
    n_rows = [0, 0, 0]
    blen = len(button_list)
    keyboard = []
    if blen == 0:
        pass
    elif blen < 10:
        for i in range(0,blen):
            n_rows[i % 3] = n_rows[i % 3] + 1
        n = 0
        keyboard = [[0] * n_rows[0], [0] * n_rows[1], [0] * n_rows[2]]
        for l in range(3):
            j = n_rows[l]
            for k in range(0, j):
                keyboard[l][k] = button_list[n]
                n += 1
    else:
        create_markup(button_list[:8], sh_id)
#        TODO - correctly creating markup for > 9 folders
#        start = (num-1)*9
#        stop = blen if blen <= num*9 else num*9
#        for i in range(0, stop%9-1):
#            n_rows[i % 3] = n_rows[i % 3] + 1
#        n = start
#        keyboard = [[0] * n_rows[0], [0] * n_rows[1], [0] * n_rows[2]]
#        for l in range(3):
#            j = n_rows[l]
#            for k in range(0, j):
#                keyboard[l][k] = button_list[n]
#                n += 1
    if pickle_read(sh_id, "is_expl_on") == True:
        keyboard.append(["Back", "Done", "More"])
    else:
        keyboard.append(['Choose folder', 'Cancel'])
    return keyboard


def explorer(id, next_dir):
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


def pickle_write(id, param_name, state):
    root_dir = os.getcwd()
    os.chdir("users_storage")
    name = 'pickle_{0}_{1}.txt'.format(id, param_name)
    print("Going to write in {3}\\{0} value: {1} : {2}".format(name, param_name, state, os.getcwd()))
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
print(pickle_read(332761,'favorites'))
