# -*- coding: utf-8 -*-
import math

button_list = [x for x in range(14)]
pg_num = 2
print(button_list)
blen = len(button_list)
keyboard = []
boobs = 9 #not my fetish, just max number of Buttons On One Board Setting =) 
start = (pg_num-1)*boobs
stop =  min(pg_num*boobs, blen) #pg_num*boobs if blen > boobs else blen
print(str(start) + ", " + str(stop))
buttons_on_page_list = button_list[start:stop]
print(buttons_on_page_list)

#num_rows = int(math.ceil(len(buttons_on_page_list)/math.sqrt(boobs)))
#num_in_last_row = len(buttons_on_page_list)-(num_rows-1)*math.sqrt(boobs)
#kb = [[x for x in range(int(math.sqrt(boobs)))] for y in range(num_rows)]
#kb.append([x for x in range(num_rows*int(math.sqrt(boobs)), len(buttons_on_page_list))])
#print("%d ___ %d" % (num_rows, num_in_last_row))
#print(kb)
#kb = [[x]]
keyboard = [[buttons_on_page_list[x+y*3] for x in range(len(buttons_on_page_list[(y-1)*]))] for y in range(int(math.ceil(len(buttons_on_page_list)/math.sqrt(boobs))))]
#print(keyboard)