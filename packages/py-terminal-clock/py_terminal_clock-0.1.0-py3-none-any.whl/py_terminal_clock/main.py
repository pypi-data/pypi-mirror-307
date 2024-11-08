import datetime
import os
import time

import pyfiglet


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

while(True):
    clear_screen()
    print('\033[?25l', end="")z z
    time_string = datetime.datetime.now().strftime('%I:%M %p').strip("0")
    time_string = " " + " ".join(time_string) #.replace(" M", "M")
    print("\n" * 10)
    large_time_string = pyfiglet.figlet_format(time_string, font= "STANDARD")
    print(large_time_string)
    time.sleep(10)
    