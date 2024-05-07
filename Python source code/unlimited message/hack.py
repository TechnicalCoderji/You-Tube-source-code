import pyautogui as pg
import time

message = input("enter message:")
t=int(input("enter how many time:"))
print("starting in 5 sec....")
time.sleep(5)
for i in range(t):
	pg.write(message)
	pg.press("enter")