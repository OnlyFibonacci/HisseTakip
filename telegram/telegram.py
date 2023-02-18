import telebot
from veritabani import*
from tradingview_ta import TA_Handler, Interval
from telegram.tvVeri import gorselLinkGetir as gg, temel
from mesajlar import Mesajlar


bot = telebot.TeleBot("TELEGRAM_BOT_TOKEN", parse_mode="HTML")


#! Kullanıcı ilk kayıt yaptığı esnada veritabanında kontrol edilir. Varsa kayıt olabilir.
@bot.message_handler(commands=['start'])
def hosgeldin(message):
    user_id = message.from_user.id
    if varMi(str(user_id),'id') == 0 :
        bot.reply_to(message, Mesajlar.hosGeldin)
        kullaniciKaydet(str(user_id),0,imlec)
    else :
        bot.reply_to(message, Mesajlar.zatenKayit)


def hisseMi(message):
    try:
        mesaj = message.text.split()
        if len(mesaj)==2:
            return True
        else:
            return False
    except:
        pass

def adminMi(message):
    try:
        user_id = message.from_user.id
        if user_id == "TELEGRAM_BOT_ADMIN_ID":
            return True
        else:
            return False
    except:
            return False



def emoji(recommendation):
    try:
        if recommendation == "NEUTRAL":
            return "⚪"
        elif recommendation == "BUY":
            return "🟢"
        elif recommendation == "SELL":
            return "🔴"
    except:
        pass


def intervalBTNekle():
    try:
        buttons = telebot.types.InlineKeyboardMarkup(row_width=3)
        btn_1 = telebot.types.InlineKeyboardButton('1m', callback_data='1m')
        btn_2 = telebot.types.InlineKeyboardButton('5m', callback_data='5m')
        btn_3 = telebot.types.InlineKeyboardButton('15m', callback_data='15m')
        btn_4 = telebot.types.InlineKeyboardButton('30m', callback_data='30m')
        btn_5 = telebot.types.InlineKeyboardButton('1h', callback_data='1h')
        btn_6 = telebot.types.InlineKeyboardButton('2h', callback_data='2h')
        btn_7 = telebot.types.InlineKeyboardButton('4h', callback_data='4h')
        btn_8 = telebot.types.InlineKeyboardButton('1d', callback_data='1d')
        btn_9 = telebot.types.InlineKeyboardButton('1w', callback_data='1w')
        # btn_10 = telebot.types.InlineKeyboardButton(reklamSec(imlec), callback_data='trx_address')
        buttons.add(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, btn_7, btn_8, btn_9)

        return buttons
    except:
        pass



def intervalSec(data):
    try:
        if data == '1m':
            return Interval.INTERVAL_1_MINUTE
        if data == '5m':
            return Interval.INTERVAL_5_MINUTES
        if data == '15m':
            return Interval.INTERVAL_15_MINUTES
        if data == '30m':
            return Interval.INTERVAL_30_MINUTES
        if data == '1h':
            return Interval.INTERVAL_1_HOUR
        if data == '2h':
            return Interval.INTERVAL_2_HOURS
        if data == '4h':
            return Interval.INTERVAL_4_HOURS
        if data == '1d':
            return Interval.INTERVAL_1_DAY
        if data == '1w':
            return Interval.INTERVAL_1_WEEK
    except:
        pass



def periyotAdi(data):
    try:
        karakterler = data
        karakterSayisi = len(karakterler)

        if karakterSayisi == 2:
            if karakterler[karakterSayisi - 1] == 'm':
                return f'{karakterler[0]} Dakika'
            if karakterler[karakterSayisi - 1] == 'h':
                return f'{karakterler[0]} Saat'
            if karakterler[karakterSayisi - 1] == 'd':
                return f'{karakterler[0]} Gün'
            if karakterler[karakterSayisi - 1] == 'w':
                return f'{karakterler[0]} Hafta'
        if karakterSayisi == 3:
            if karakterler[karakterSayisi - 1] == 'm':
                return f'{karakterler[0]}{karakterler[1]} Dakika'
            if karakterler[karakterSayisi - 1] == 'h':
                return f'{karakterler[0]}{karakterler[1]} Saat'
            if karakterler[karakterSayisi - 1] == 'd':
                return f'{karakterler[0]}{karakterler[1]} Gün'
            if karakterler[karakterSayisi - 1] == 'w':
                return f'{karakterler[0]}{karakterler[1]} Hafta'
    except:
        pass



@bot.message_handler(commands=['izinliGrupEkle'],func=adminMi)
def izinliGrup(message):
    try:
        grupid = message.text.split()[1]
        izinliGrupEkle(str(grupid),imlec)
        
    except:
        bot.reply_to(message, "Eklenemedi")


@bot.message_handler(commands=['komutlar'])
def komutlariYaz(message):
    yazi = """
    /sorgu - Bugün kaç sorgu yaptığınızı, toplam kaç sorgu yaptığınızı ve günlük kaç sorgu hakkınız kaldığını gösterir.\n/temel THYAO - Bu sorguda THYAO hissesinin temel analiz verilerini alacaksınız.\n/teknik THYAO - Bu sorguda THYAO hissesinin teknik analiz verilerini alacaksınız.\n/grafik THYAO - Bu sorguda kullanıcıların THYAO hissesine ait paylaştığı grafikleri göreceksiniz.\n/id - Telegram ID'nizi size gönderir.\n
    """
    bot.reply_to(message, yazi)

@bot.message_handler(commands=['id'])
def idGonder(message):
    bot.reply_to(message, f"Telegram ID'niz : {message.chat.id}")





@bot.message_handler(commands=['kacKisi'],func=adminMi)
def kisiSayisi(message):
    try:
        bot.reply_to(message,f"Bu botu kullanan kişi sayısı : {kacKisi()}\nToplam Yapılan Sorgu : {butunSorgular()}")
    except:
        pass

@bot.message_handler(commands=['reklamSayisi'],func=adminMi)
def reklamSayi(message):
    try:
        bot.reply_to(message,f"Reklam Sayısı : {reklamSayisi()}")
    except:
        pass

@bot.message_handler(commands=['reklamSil'],func=adminMi)
def reklamSil(message):
    try:
        reklamlariSil()
        bot.reply_to(message,"Reklamlar silindi.")
    except:
        pass


@bot.message_handler(commands=['duyuru'],func=adminMi)
def duyuruGec(message):
    try:
        idler = kullananKisilerinIdleri()
        duyuru = message.text.split('duyuru')[1]
        for i in idler :
            bot.send_message(i[0],duyuru)
    except :
        pass


@bot.message_handler(commands=['reklamEkle'],func=adminMi)
def reklamEkle(message):
    try:
        reklam = message.text.split('reklamEkle')[1]
        reklamEkleDb(str(reklam),imlec)
    except:
        pass

@bot.message_handler(commands=['sifirla'],func=adminMi)
def sifirla(message):
    try:
        haklariSifirla()
        bot.reply_to(message,"Herkesin günlük sorgu sayısı 0'landı.")
    except:
        bot.reply_to(message,Mesajlar.hataMesaji)

@bot.message_handler(commands=['izinGuncelle'], func=adminMi)
def izinAyarla(message):
    try:
        kelimeler = message.text.split()
        guncellenecekIzin = kelimeler[1]
        yeniHakSayisi = kelimeler[2]
        izinHakGuncelle(int(guncellenecekIzin), int(yeniHakSayisi),imlec)
        bot.reply_to(message,Mesajlar.guncellendi)
    except:
        bot.reply_to(message,Mesajlar.guncellenemedi)

@bot.message_handler(commands=['yetkiGuncelle'], func=adminMi)
def yetkiGuncelle(message):
    try:
        kelimeler = message.text.split()
        kullaniciId = kelimeler[1]
        yeniYetki = kelimeler[2]
        kullaniciYetkiDuzenle(str(kullaniciId), int(yeniYetki),imlec)
        bot.reply_to(message,Mesajlar.guncellendi)
    except:
        bot.reply_to(message,Mesajlar.guncellenemedi)


@bot.message_handler(commands=['izinGrubuEkle'], func=adminMi)
def izinGrubuEkle(message):
    try:
        kelimeler = message.text.split()
        yeniIzinId = kelimeler[1]
        yeniSorguHakki = kelimeler[2]
        yeniIzinGrubuEkle(int(yeniIzinId), int(yeniSorguHakki),imlec)
        bot.reply_to(message,Mesajlar.eklendi)
    except:
        bot.reply_to(message,Mesajlar.eklenemedi)

       
@bot.message_handler(commands=['sorgu'])
def sorguHakkiGonder(message):
    try:
        user_id = message.from_user.id
        yapilanSorgu = sorguSayisi(user_id,imlec)
        kalanSorguHakki = izinSorgula(user_id,imlec) - yapilanSorgu
        toplam = toplamSorguSayisi(user_id,imlec)
        bot.reply_to(message,f"Bugün Yaptığınız Sorgu : {yapilanSorgu}\nKalan Sorgu : {kalanSorguHakki}\nToplam Yaptığınız Sorgu : {toplam}")
    except:
        bot.reply_to(message,Mesajlar.hataMesaji)


    



@bot.message_handler(commands=['temel'])
def temelGonder(message):
    try: 
        user_id = message.from_user.id
        kelimeSayisi = len(message.text.split())
        if varMi(str(user_id),'id') == 0 :
            kullaniciKaydet(str(user_id),0,imlec)
                    
        if kelimeSayisi==1:
            bot.reply_to(message,"/temel THYAO - yazarak hissenin temel analiz verilerini görebilirsiniz.")
        elif kelimeSayisi==2:
            if sorguSayisi(user_id,imlec) < izinSorgula(user_id,imlec):
                request = message.text.split()[1]
                temelVeri = temel(request.upper())
                bot.reply_to(message,temelVeri)
                sorguArttir(str(user_id),imlec)
                sorgu = sorguSayisi(str(user_id),imlec)
                kalanHak = izinSorgula(user_id,imlec) - sorguSayisi(user_id,imlec) 
                bot.send_message(message.chat.id,  f"\nSorgu Sayısı : {sorgu}\nKalan Sorgu Hakkı : {kalanHak}")
                if reklamSayisi() > 0 and izinGetir(user_id,imlec) != 1:
                    bot.send_message(message.chat.id,str(reklamSec()))
            else:
                bot.reply_to(message, Mesajlar.sorguHakkiKalmadi)
                yapilanSorgu = sorguSayisi(user_id,imlec)
                kalanSorguHakki = izinSorgula(user_id,imlec) - yapilanSorgu
                bot.reply_to(message,f"Yaptığınız Sorgu : {yapilanSorgu}\nKalan Sorgu : {kalanSorguHakki}")
        else:
            bot.reply(message,Mesajlar.sorguyuDuzelt)
    except:
        bot.reply_to(message,Mesajlar.bulamadim)
        
@bot.message_handler(commands=['grafik'])
def grafikGonder(message):
    try:
        user_id = message.from_user.id
        kelimeSayisi = len(message.text.split())
        if varMi(str(user_id),'id') == 0 :
            kullaniciKaydet(str(user_id),0,imlec)
        if kelimeSayisi==1:
            bot.reply_to(message,"/grafik THYAO - yazarak hissenin tradingview'de paylaşılan grafiklerini görebilirsiniz.")
        elif kelimeSayisi==2:
            if sorguSayisi(user_id,imlec) < izinSorgula(user_id,imlec):
                request = message.text.split()[1]
                gorseller = gg(request.upper())
                uyarli = []
                user_id = message.from_user.id
                for i in gorseller:
                    uyarli.append(telebot.types.InputMediaPhoto(i,"Bu grafikler, tradingview sitesinde paylaşım yapan kullanıcılara aittir."))
                bot.send_media_group(message.chat.id,uyarli)
                sorguArttir(str(user_id),imlec)
                sorgu = sorguSayisi(str(user_id),imlec)
                kalanHak = izinSorgula(user_id,imlec) - sorguSayisi(user_id,imlec) 
                bot.send_message(message.chat.id,  f"\nSorgu Sayısı : {sorgu}\nKalan Sorgu Hakkı : {kalanHak}")
                if reklamSayisi() > 0 and izinGetir(user_id,imlec) != 1:
                    bot.send_message(message.chat.id,str(reklamSec()))

            else:
                bot.reply_to(message, Mesajlar.sorguHakkiKalmadi)
                yapilanSorgu = sorguSayisi(user_id,imlec)
                kalanSorguHakki = izinSorgula(user_id,imlec) - yapilanSorgu
                bot.reply_to(message,f"Yaptığınız Sorgu : {yapilanSorgu}\nKalan Sorgu : {kalanSorguHakki}")
            
        else:
            bot.reply(message,Mesajlar.sorguyuDuzelt)
    except:
        bot.reply_to(message,Mesajlar.bulamadim)


@bot.message_handler(commands=['teknik'])
def hisse(message, zaman='1h'):
    try:
        
        user_id = message.from_user.id
        kelimeSayisi = len(message.text.split())
        if varMi(str(user_id),'id') == 0 :
            kullaniciKaydet(str(user_id),0,imlec)
        if kelimeSayisi==1:
            bot.reply_to(message,"/teknik THYAO - yazarak hissenin teknik verilerini görebilirsiniz.")
        elif kelimeSayisi==2:
            if sorguSayisi(user_id,imlec) < izinSorgula(user_id,imlec):
                request = message.text.split()[1]
                coin = TA_Handler(symbol=request.upper(), screener="turkey", exchange="BIST",
                                interval=intervalSec(zaman))
                ind = coin.get_analysis().indicators
                price = coin.get_analysis().indicators['close']
                rec = coin.get_analysis().oscillators['COMPUTE']
                ma = coin.get_analysis().indicators
                recMa = coin.get_analysis().moving_averages['COMPUTE']
                ma_s = f"\n{emoji(recMa['SMA20'])}SMA20 : {round(ma['SMA20'],2)}\n{emoji(recMa['SMA50'])}SMA50 : {round(ma['SMA50'],2)}\n{emoji(recMa['SMA100'])}SMA100 : {round(ma['SMA100'],2)}\n{emoji(recMa['SMA200'])}SMA200 : {round(ma['SMA200'],2)}\n###############\n" \
                    f"{emoji(recMa['EMA20'])}EMA20 : {round(ma['EMA20'],2)}\n{emoji(recMa['EMA50'])}EMA50 : {round(ma['EMA50'],2)}\n{emoji(recMa['EMA100'])}EMA100 : {round(ma['EMA100'],2)}\n{emoji(recMa['EMA200'])}EMA200 : {round(ma['EMA200'],2)}"
                
                ind_s = f"Hisse Adı : {request.upper()}\nPeriyot : {periyotAdi(zaman)}\n###############\nFiyat : {price}\n{ma_s}\n###############\n{emoji(rec['RSI'])} RSI : {round(ind['RSI'],2)}\n{emoji(rec['CCI'])} CCI20 : {round(ind['CCI20'],2)} \n{emoji(rec['ADX'])} ADX : {round(ind['ADX'],2)}\n{emoji(rec['AO'])} AO : {round(ind['AO'],2)} \n{emoji(rec['Mom'])} MOM : {round(ind['Mom'],2)}\n{emoji(rec['W%R'])} WilliamsR {round(ind['W.R'],2)}\n⚪ Volume : {round(ind['volume'],2)}\n"
                
                sorguArttir(str(user_id),imlec)
                sorgu = sorguSayisi(str(user_id),imlec)
                kalanHak = izinSorgula(user_id,imlec) - sorguSayisi(user_id,imlec) 
                bot.send_message(message.chat.id, ind_s + f"\nSorgu Sayısı : {sorgu}\nKalan Sorgu Hakkı : {kalanHak}", reply_markup=intervalBTNekle())
                if reklamSayisi() > 0 and izinGetir(user_id,imlec) != 1:
                    bot.send_message(message.chat.id,str(reklamSec()))

            else:
                bot.reply_to(message, Mesajlar.sorguHakkiKalmadi)
                yapilanSorgu = sorguSayisi(user_id,imlec)
                kalanSorguHakki = izinSorgula(user_id,imlec) - yapilanSorgu
                bot.reply_to(message,f"Yaptığınız Sorgu : {yapilanSorgu}\nKalan Sorgu : {kalanSorguHakki}")
        else:
            bot.reply(message, Mesajlar.sorguyuDuzelt)
            
    except:
        bot.reply_to(message,Mesajlar.bulamadim)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        mid = call.message.message_id
        mtext=call.message.text
        hisse = call.message.text.split()[3]
        cesit = call.message.text.split()[0]  # tür
        periyot = call.data
        if cesit.lower() == 'hisse':
            try:
                request = hisse
                zaman = periyot
                coin = TA_Handler(symbol=request.upper(), screener="turkey", exchange="BIST",
                                    interval=intervalSec(zaman))
                ind = coin.get_analysis().indicators
                price = coin.get_analysis().indicators['close']
                rec = coin.get_analysis().oscillators['COMPUTE']
                ma = coin.get_analysis().indicators
                recMa = coin.get_analysis().moving_averages['COMPUTE']
                ma_s = f"\n{emoji(recMa['SMA20'])}SMA20 : {round(ma['SMA20'],2)}\n{emoji(recMa['SMA50'])}SMA50 : {round(ma['SMA50'],2)}\n{emoji(recMa['SMA100'])}SMA100 : {round(ma['SMA100'],2)}\n{emoji(recMa['SMA200'])}SMA200 : {round(ma['SMA200'],2)}\n##########\n" \
               f"{emoji(recMa['EMA20'])}EMA20 : {round(ma['EMA20'],2)}\n{emoji(recMa['EMA50'])}EMA50 : {round(ma['EMA50'],2)}\n{emoji(recMa['EMA100'])}EMA100 : {round(ma['EMA100'],2)}\n{emoji(recMa['EMA200'])}EMA200 : {round(ma['EMA200'],2)}"
                
                ind_s = f"Hisse Adı : {request.upper()}\nPeriyot : {periyotAdi(zaman)}\n###############\nFiyat : {price}\n{ma_s}\n###############\n{emoji(rec['RSI'])} RSI : {round(ind['RSI'],2)}\n{emoji(rec['CCI'])} CCI20 : {round(ind['CCI20'],2)} \n{emoji(rec['ADX'])} ADX : {round(ind['ADX'],2)}\n{emoji(rec['AO'])} AO : {round(ind['AO'],2)} \n{emoji(rec['Mom'])} MOM : {round(ind['Mom'],2)}\n{emoji(rec['W%R'])} WilliamsR {round(ind['W.R'],2)}\n⚪ Volume : {round(ind['volume'],2)}\n"
                # bot.send_message(cid, ind_s, reply_markup=intervalBTNekle())
                sorgu = sorguSayisi(str(cid),imlec)
                kalanHak = izinSorgula(cid,imlec) - sorgu
                bot.edit_message_text(message_id=mid, chat_id=cid, text=ind_s+ f"\nSorgu Sayısı : {sorgu}\nKalan Sorgu Hakkı : {kalanHak}", reply_markup=intervalBTNekle())
            except:
                pass
    except:
        pass            








#! Bot sürekli çalışıyor
def botCalistir():
    bot.infinity_polling()



# #! Bu komut ile kullanıcı hisse ekleyebilecek.
# @bot.message_handler(commands=['ekle'])
# def ekle(message):
#     user_id = message.from_user.id
#     yazi = message.text
#     if len(yazi.split(" ")) > 2 : 
#         bot.reply_to(message,"Lütfen sadece bir hisse adı giriniz.\nÖrneğin : /ekle THYAO")
#     elif len(yazi.split(" ")) == 2 : 
#         bot.reply_to(message,"Hisse başarıyla takip listesine eklendi.")
#     else:
#         bot.reply_to(message,"Lütfen bu komutun sonuna bir hisse adı ekleyin.\nÖrneğin : /ekle THYAO")
