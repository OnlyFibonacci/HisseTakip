import veritabani
from telegram.telegram import botCalistir
import zamanKontrol


import threading

thread1 = threading.Thread(target=botCalistir)
thread2 = threading.Thread(target=zamanKontrol.zaman)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

