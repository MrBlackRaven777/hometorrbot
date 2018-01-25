# -*- coding: utf-8 -*-
import math

button_list = [x for x in range(25)]
pg_num = 2
blen = len(button_list)
keyboard = []
boobs =  16#not my fetish, just max number of Buttons On One Board Setting =) 
start = (pg_num-1)*boobs
stop =  min(pg_num*boobs, blen)
buttons_on_page_list = button_list[start:stop]

sqrb = int(math.sqrt(boobs))
keyboard = [[buttons_on_page_list[x+y*sqrb] for x in range(min(sqrb, len(buttons_on_page_list)-y*sqrb))] for y in range(int(math.ceil(len(buttons_on_page_list)/sqrb)))]
print(keyboard)
