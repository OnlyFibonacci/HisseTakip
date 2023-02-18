import datetime
from veritabani import haklariSifirla
import locale

sunucuKonum = locale.getlocale()[0]

def zaman():
    while True:
        bugun = datetime.datetime.today()
        fark = datetime.timedelta(hours=3) if sunucuKonum != "Turkish_Turkey" else datetime.timedelta(hours=0)
        tr = bugun + fark
        saat = tr.hour
        dakika = tr.minute
        if saat == 0 and dakika == 15:
            haklariSifirla()
            
        


