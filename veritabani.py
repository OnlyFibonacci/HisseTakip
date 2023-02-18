import sqlite3

def veriTabaniBaglan(dosyaAdi:str):
    return sqlite3.connect(f'{dosyaAdi}.db',check_same_thread=False)
    #.db uzantısını istediğim gibi değiştirebilirim. Yoksa oluştur varsa bağlan

def imlecOlustur(db):
    return db.cursor()
    #db değişkenine oluşturulan veritabanını gönder.

def degisiklikleriKaydet(db):
    db.commit()

database = veriTabaniBaglan('veritabani')
imlec = imlecOlustur(database)
 
 
def varMi(veri,sutun):
    #return imlec.execute(f"SELECT * FROM telegram WHERE {sutun} = '{veri}'")
    return imlec.execute(f"SELECT COUNT(*) FROM telegram WHERE {sutun} = '{veri}'").fetchone()[0]

def butunSorgular():
    return imlec.execute("SELECT SUM(toplamSorgu) FROM telegram").fetchone()[0]
   

  

def kacKisi():
    return imlec.execute("SELECT COUNT(*) FROM telegram").fetchone()[0]

def kullananKisilerinIdleri():
    return imlec.execute("SELECT id FROM telegram").fetchall()
  
def kullaniciKaydet(kullaniciId:str,izin,imlec):
    imlec.execute(f'INSERT INTO telegram VALUES ({kullaniciId},{izin},0,0)')
    degisiklikleriKaydet(database)
    
def sorguArttir(kullaniciId:str,imlec):
    imlec.execute(f"UPDATE telegram SET sorguSayisi = sorguSayisi + 1 WHERE id = {kullaniciId}")
    imlec.execute(f"UPDATE telegram SET toplamSorgu = toplamSorgu + 1 WHERE id = {kullaniciId}")

    degisiklikleriKaydet(database)

def sorguSayisi(kullaniciId:str,imlec):
    imlec.execute(f"SELECT * FROM telegram WHERE id = {kullaniciId}")
    return imlec.fetchone()[2]

def toplamSorguSayisi(kullaniciId:str,imlec):
    imlec.execute(f"SELECT * FROM telegram WHERE id = {kullaniciId}")
    return imlec.fetchone()[3]

def izinGetir(kullaniciId:str,imlec):
    imlec.execute(f"SELECT * FROM telegram WHERE id = {kullaniciId}")
    return imlec.fetchone()[1]

def izinSorgula(kullaniciId:str,imlec):
    yetkiNo = izinGetir(kullaniciId,imlec)
    return imlec.execute(f"SELECT * FROM izinler WHERE id = {yetkiNo}").fetchone()[1]

def izinHakGuncelle(izinId,yeniHak,imlec):
    imlec.execute("UPDATE izinler SET sorguSayisi = ? WHERE id = ?",(yeniHak,izinId))
    degisiklikleriKaydet(database)

def kullaniciYetkiDuzenle(kullaniciId:str,yeniYetki:int,imlec):
    imlec.execute("UPDATE telegram SET izin = ? WHERE id = ?",(yeniYetki,kullaniciId))
    degisiklikleriKaydet(database)

def yeniIzinGrubuEkle(ids:str,sorguHakki:int,imlec):
    if not imlec.execute(f"SELECT * FROM izinler WHERE id = {ids}").fetchone() :
        imlec.execute('INSERT INTO  izinler VALUES (?,?)',(ids,sorguHakki))
        degisiklikleriKaydet(database)

def reklamEkleDb(reklam:str,imlec):
    imlec.execute('INSERT INTO reklamlar VALUES (?)',(reklam,))
    degisiklikleriKaydet(database)

def reklamSec():
    return imlec.execute('SELECT metin FROM reklamlar ORDER BY RANDOM() LIMIT 1').fetchone()[0]

def reklamSayisi():
    return imlec.execute("SELECT COUNT(*) FROM reklamlar").fetchone()[0]
    
def reklamlariSil():
    imlec.execute("DELETE FROM reklamlar WHERE metin IS NOT NULL")
    degisiklikleriKaydet(database)



def izinliGrupEkle(ids:str,imlec):
    if not imlec.execute(f"SELECT * FROM gruplar WHERE id = {ids}").fetchone():
        imlec.execute(f'INSERT INTO gruplar VALUES ({ids},0,0)')
        degisiklikleriKaydet(database)
def haklariSifirla():
    imlec.execute("UPDATE telegram SET sorguSayisi = 0")
    degisiklikleriKaydet(database)


# telegram tablosu oluşturuldu
imlec.execute("CREATE TABLE IF NOT EXISTS telegram (id text, izin int, sorguSayisi int, toplamSorgu int)")
imlec.execute("CREATE TABLE IF NOT EXISTS izinler (id int,  sorguSayisi int)")
imlec.execute("CREATE TABLE IF NOT EXISTS gruplar (id text,  sorguSayisi int, toplamSorgu int)")
imlec.execute("CREATE TABLE IF NOT EXISTS reklamlar (metin text)")

def izinEkle():
    imlec.execute('INSERT INTO  izinler VALUES (0,20)')
    imlec.execute('INSERT INTO  izinler VALUES (1,40)')
    imlec.execute('INSERT INTO  izinler VALUES (2,50)')
    imlec.execute('INSERT INTO  izinler VALUES (9,9999)')



izinEkle()
degisiklikleriKaydet(database)


