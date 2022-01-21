# -*- coding: utf-8 -*-
import glob
import os
import re
#моя библеотека для парсинга фото
from parser import GetLinkPhoto, GetPhoto
#импорт ботапи, типов ботаапи и работу с картинками
import telebot
from PIL import Image
from telebot import types

from constants import token
from func import DesktopMobile, Stats
from img import ChoiceConvertImg

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def Welcome(message):
    #скидываем все файлы(настройки) до стоковых значений
    bot.send_message(message.chat.id, "Привет, я твой личный помощник для постинга картинок в каналы."  + "\n" + "Отправь /help для полного списка команд.")
    #канал в который будет все отправляться
    open('config/ChanelTarget.txt', 'w')
    #айди фото для отправки в канал
    open('config/IDPhotoChanel.txt', 'w').write('0')
    #айди фото для отправки в лс с ботом
    open('config/IDPhotoNow.txt', 'w').write('1')
    #скаченые страницы
    open('config/NumberPage.txt', 'w', encoding="utf-8").write('Последняя страница сайта 1: 0' + '\n'
                                             'Последняя страница сайта 2: 0' + '\n'
                                             'Последняя страница сайта 3: 0' + '\n'
                                             'Последняя страница сайта 4: 0' + '\n'
                                             'Последняя страница сайта 5: 0' + '\n')

@bot.message_handler(commands=['key'])
def Keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    item1 = types.KeyboardButton("n0white wallpapers")
    item2 = types.KeyboardButton("n0nime")

    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Клавиатура активированна.", reply_markup=markup)

@bot.message_handler(commands=['help'])
def Help(message):
    bot.send_message(message.chat.id,
        "Привет, это помощь по боту. Ознакомся с ней внимательно, и лучше не делай так, как не надо, я мог что то упустить, ибо не супер опытный программист :)" + '\n' + '\n' +
        "Напиши команду /startpost (номер страницы, до которой нужно скачивать) (напиши сайт с которого скачивать)." + '\n' +
        "/startpost 10 1 (Скачает с 1-й страницы до 10-й у 1-го сайта)." + '\n' + '\n' +
        "Команда /start сбрасывает всю информацию о тебе и каналах, приедтся еще раз писать ее." + '\n' +
        "Но, это полезно, потому что на сайтах добовляются новые фотографии каждый день." + '\n' + '\n' +
        "Команда /regchannel (ID канала) запишет канал (можно менять этой командой каналы), в который будут выкладываться фотографии." + '\n' +
        "/regchannel -1001255908484 (будет записан данный канал)" + '\n' + '\n' +
        "Команда /delphoto удаляет все фото из папки и сбрасывает ID фотографий (если написать, то бот будет работать быстрее, если ID был большим числом, к примеру 2000)." + '\n' +
        "n0walls_(тут айди).png" + '\n' +
        "Команда /stats просто выводит статистику, имхо интересно чекать." + '\n' +
        "Команда /idphoto устанавливает ID картинки с которого будут начится посты в канале."  + '\n' + '\n' +
        "Сайт 1: https://unsplash.com/t/wallpapers" + '\n' +
        "Сайт 2: https://unsplash.com/t/textures-patterns" + '\n' + 
        "Сайт 3: https://unsplash.com/wallpapers/phone" + '\n' +
        "Сайт 4: https://akspic.ru/ (здесь скачивается в 2-х страниц сразу на телефон и ПК)" + '\n' + '\n' +
        "Сайт 5: https://wallhaven.cc/search?categories=100&purity=100&sorting=date_added&order=desc&page=1" + '\n' + '\n' +
        "За один раз лучше не скачивать больше 10 страниц, сайт может отклонить запрос." + '\n' +
        "Во время отправи ботом фотографий после скачивания, лучше не трогать его, он может работать не правильно, потому что он не асинхронный." + '\n' +
        "Также во время отправки фото в канал ничего не делай, просто жди - это не долго. Сверху экрана в чате будет написанно \"загрузка...\"" + '\n' +
        "Можно дальше нажимать лайки, когда фото уже отправлено в канал. Можешь попробовать нажимать несколько подряд, но не думаю, что сработает, если, что просто напиши /start." + '\n' +
        "Когда фото отправляется в канал, оно удаляется из папки, при дизлайке также удаляется." + '\n' +
        "Иногда бывает, что бот отправляет не все фотографии - это нормально, они могут не подходить по размерам для отправки, так как есть ограничения или они весят больше 10мб." + '\n' +
        "Также бот может не запостить фото без сжатия, потому что оно весит больше 10мб." + '\n' +
        "Скорость работы бота зависит от серверов телеграмма и твоей скорости интрнета." + '\n' +
        "Если будут ошибки, то скидывай мне все последние фидбеки с консоли и опиши действия, которые ты делал." + '\n' +
        "Можешь ошибки в переводчик скидывать и смотреть, что там, думаю разберешься." + '\n' +
        "В консоли могут появляться ошибки, но если по факту бот работатет, то и нормально все." + '\n' +
        "Если что пиши @NoverLove")

@bot.message_handler(commands=['stats'])
def OutputStats(message):
    #читаем скаченые страницы и документ статы, и выводим все
    dowsite = open('config/NumberPage.txt', 'r', encoding="utf8").read()
    statsbot = open('config/Stats.txt', 'r').readlines()
    bot.send_message(message.chat.id, 
    "Скаченные страницы:" + '\n' + dowsite + '\n' +
    "Скачано фотографий: " + statsbot[0] +
    "Лайкнутых фотографий: " + statsbot[1] +
    "Дизлайкнутых фотографий: " + statsbot[2] +
    "Отправленых фотографий: " + statsbot[4] +
    "Не отправленых фотографий: " + statsbot[3])

@bot.message_handler(commands=['delphoto'])
def delphoto(message):
    #делаем клаву и отправляем
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("👍", callback_data='del')
    item2 = types.InlineKeyboardButton("👎", callback_data='notdel')

    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Ты точно хочешь удалить все файлы из папки photos?", reply_markup=markup)

@bot.message_handler(commands=['idphoto'])
def IdPhoto(message):
    #записывает айди фото для канала
    try:
        # если указанное число больше или равно 0, то запишим в файл (айди для канал) это число
        if int(message.text.split()[1]) - 1 >= 0:
            open('config/IDPhotoChanel.txt', 'w').write(str(int(message.text.split()[1]) - 1))
            bot.send_message(message.chat.id, "Я записал. Ты сможешь изменить это в любой момент.")
        else: bot.send_message(message.chat.id, "Укажите число больше или равное 1")
    except: bot.send_message(message.chat.id, "Укажите через пробел ID картинок с котогоро будут начинаться посты.")

@bot.message_handler(commands=['regchannel'])
def Registration(message):
    try:
        #записываем айди канала
        open('config/ChanelTarget.txt', 'w').write(message.text.split()[1])
        bot.send_message(message.chat.id, "Успешно добавлено.")
    except: bot.send_message(message.chat.id, "Укажи через пробел ID канала, куда будут выкладываться картинки.")

@bot.message_handler(commands=['startpost'])
def StartPost(message):
    #Если написали без параметров
    if len(message.text.split()) < 3:
        bot.send_message(message.chat.id, "Нужно указать еще параметры для работы бота.")
        return False
    elif not str(message.text.split()[1]).isdigit() or not str(message.text.split()[2]).isdigit():
        bot.send_message(message.chat.id, 'Недопустимые символы или вы написали не коректно.')
        return False
    #если сайта нету
    elif int(message.text.split()[2]) > 5:
        bot.send_message(message.chat.id, "Такого сайта не существует.")
        return False
    lastPage = open('config/NumberPage.txt', 'r', encoding="utf8").readlines()[int(message.text.split()[2]) - 1]
    #Если страница уже была скачана сообщить пользователю
    if int(lastPage[28:]) >= int(message.text.split()[1]):
        bot.send_message(message.chat.id, "Страница уже была скачана." + '\n' + lastPage)
        return False
    del lastPage
    #Клавиатура
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("👍", callback_data='good')
    item2 = types.InlineKeyboardButton("👎", callback_data='bad')

    markup.add(item1, item2)

    del item1, item2
    #Переменные для текущего айди фото для лс с ботом и колличества ошибок
    id_p = open('config/IDPhotoNow.txt', 'r').readlines()
    error = 0
    #Исключение надо ибо там 2 функции запускаются
    num_photo = len(GetPhoto(message, bot, GetLinkPhoto(message, bot, int(message.text.split()[1]), int(message.text.split()[2]))))
    #отправляет фотографии
    for i in range(num_photo, 0, -1):
        try:
            src = "photos/" + 'n0walls_' + str(int(id_p[0]) + (num_photo - i) - 1) + ".png"
            sizePhoto = re.sub(', ', 'х',  str(Image.open(src).size))
            bot.send_photo(message.chat.id, (os.path.basename(src[7:]), open(src, 'rb')), reply_markup=markup, caption=src[7:] + "\n" + "Исходное разрешение: " + sizePhoto + '\n' + DesktopMobile(sizePhoto))
        except Exception as e:
            i -= 1
            error += 1
            if str(e) not in "No such file or directory":
                pass
            else:
                print("\nStartPost-2: \n" + repr(e))
    #записывает в статистику кол-во отправленных и не отправленых фото
    Stats(error, 3)
    Stats((num_photo - error), 4)
    bot.send_message(message.chat.id, "Успешно отправленные фотографии: " + str(num_photo - error) + " штук." + '\n' + "Не отправленные фотографии: " + str(error) + " штук.")

@bot.message_handler(content_types=['document'])
def SendDoc(message):
    raw = message.document.file_id
    src = 'download_photo/nowalls.png'
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(src,'wb') as new_file:
        new_file.write(downloaded_file)

    #берем фото по пути src
    photo = open(src, 'rb').read()
    #берем айди фотографии канала
    #записываем новое значение айди фотографии для канала
    id_ = str(int(open('config/IDPhotoChanel.txt', 'r').read()) + 1)
    open('config/IDPhotoChanel.txt', 'w').write(id_)
    #читаем айди фото для отправки документа и фото в канал
    id_ = open('config/IDPhotoChanel.txt', 'r').read()
    #берем айди канала
    chanelID = open('config/ChanelTarget.txt', 'r').read()
    #размер фото - (4000х5000)
    sizePhoto = re.sub(', ', 'х',  str(Image.open(src).size))

    if chanelID == '-1001412609976':
        photo_basename = os.path.basename("n0walls_" + id_ + ".png")
        bot.send_photo(int(chanelID), (photo_basename, ChoiceConvertImg(src)), 
        caption="[n0walls](https://t.me/n0walls) " + DesktopMobile(sizePhoto), parse_mode='Markdown')
        bot.send_document(int(chanelID), (photo_basename, photo))
    elif chanelID == '-1001487239582':
        photo_basename = os.path.basename("n0nime_" + id_ + ".png")
        bot.send_photo(int(chanelID), (photo_basename, photo), 
        caption="[n0nime](https://t.me/n0nime) ", parse_mode='Markdown')
        bot.send_document(int(chanelID), (photo_basename, photo))
    else:
        photo_basename = os.path.basename("test_" + id_ + ".png")
        bot.send_photo(int(chanelID), (photo_basename, photo), 
        caption="[n0nime](https://t.me/n0nime) ", parse_mode='Markdown')
        bot.send_document(int(chanelID), (photo_basename, photo))

@bot.message_handler(content_types=['text'])
def MessageTextCall(message):
    if message.text == 'n0white wallpapers':
        open('config/ChanelTarget.txt', 'w').write('-1001412609976')
        bot.send_message(message.chat.id, "Канал успешно обновлен.")
    elif message.text == 'n0nime':
        open('config/ChanelTarget.txt', 'w').write('-1001487239582')
        bot.send_message(message.chat.id, "Канал успешно обновлен.")

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        #если лайк
        if call.data == 'good':
            #берем айди текущей фотографии
            num_photo = open('config/IDPhotoNow.txt', 'r').read()
            #записываем в статистику что лайкнули фото
            Stats(1, 1)
            #цикл для поста в канал
            for i in range(0, int(num_photo) + 1):
                try:
                    src = "photos/" + 'n0walls_' + str(i + 1) + ".png"
                    sizePhoto = re.sub(', ', 'х',  str(Image.open(src).size))
                    #если подпись под фото в лс с ботом сходится с ссылкой без "/photos" 
                    if call.message.caption == src[7:] + "\n" + "Исходное разрешение: " + sizePhoto + '\n' + DesktopMobile(sizePhoto):
                        #берем фото по пути src
                        photo = open(src, 'rb').read()
                        #берем айди фотографии канала
                        #записываем новое значение айди фотографии для канала
                        id_ = str(int(open('config/IDPhotoChanel.txt', 'r').read()) + 1)
                        open('config/IDPhotoChanel.txt', 'w').write(id_)
                        #читаем айди фото для отправки документа и фото в канал
                        id_ = open('config/IDPhotoChanel.txt', 'r').read()
                        #берем айди канала
                        chanelID = open('config/ChanelTarget.txt', 'r').read()
                        #отправляем фото с подписью и документ также
                        if chanelID == '-1001412609976':
                            photo_basename = os.path.basename("n0walls_" + id_ + ".png")
                            bot.send_photo(int(chanelID), (photo_basename, ChoiceConvertImg(src)), 
                            caption="[n0walls](https://t.me/n0walls) " + DesktopMobile(sizePhoto), parse_mode='Markdown')
                            bot.send_document(int(chanelID), (photo_basename, photo))
                        elif chanelID == '-1001487239582':
                            photo_basename = os.path.basename("n0nime_" + id_ + ".png")
                            bot.send_photo(int(chanelID), (photo_basename, photo), 
                            caption="[n0nime](https://t.me/n0nime) ", parse_mode='Markdown')
                            bot.send_document(int(chanelID), (photo_basename, photo))
                        else:
                            photo_basename = os.path.basename("test_" + id_ + ".png")
                            bot.send_photo(int(chanelID), (photo_basename, photo), 
                            caption="[n0nime](https://t.me/n0nime) ", parse_mode='Markdown')
                            bot.send_document(int(chanelID), (photo_basename, photo))
                        #удаляем фото оно не пригодится
                        os.remove(src)
                        #заканчиваем, а толку дальше его гонять ?
                        break
                except Exception as e:
                    if str(e) not in "No such file or directory":
                        pass
                    else:
                        print("callback - 2: " + repr(e))
            #удаляем смс из лс с ботом которое лайкнули
            bot.delete_message(call.message.chat.id, call.message.id)
        #если дизлайк
        elif call.data == 'bad':
            #удаляем смс ибо не красивое )
            bot.delete_message(call.message.chat.id, call.message.id)
            # записываем в статистику что нажали дизлайк
            Stats(1, 2)
            #удаляем эту некрасивую картинку
            #os.remove("photos/" + call.message.caption.split()[0])
            
        #нужен для удаления всех фото в папке photos
        elif call.data == 'del':
            #нужна для вывод кол-ва удаленных фото
            i = 0
            #обновляем значение айди фото для лс с ботом
            open('config/IDPhotoNow.txt', 'w').write('1')
            #сидим удаляем по 1-й фотке
            for f in glob.glob('photos/*'):
                os.remove(f)
                i += 1
            bot.send_message(call.message.chat.id, "Было удалено: " + str(i) + " файлов.")

            bot.delete_message(call.message.chat.id, call.message.id)
        #если передумали все таки
        elif call.data == 'notdel': 
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, "Вот и славно :)")
#запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)