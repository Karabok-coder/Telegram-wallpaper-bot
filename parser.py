# -*- coding: utf-8 -*-
import re
import types
import requests
from bs4 import BeautifulSoup
from constants import sites, s_last_1, s_last_2, s_last_3, headers

#для получения ссылок для скачивания фото
def GetLinkPhoto(message, bot, before_, sitenum):
    #сохраняет фото
    photo = []
    #читаем последний номер страницы
    last = open('config/NumberPage.txt', 'r', encoding="utf8").readlines()
    per = open('config/NumberPage.txt', 'w', encoding="utf8")
    #отправляем номер последней страницы   
    bot.send_message(message.chat.id, last[sitenum - 1])
    #от последней странцы до новой вызываем функцию для скачивания страницы сразу ее 
    #ищем нужные ссылки и добавляем в список для 3-й ссылки другое выраженние
    for i in range(int(last[sitenum - 1][28:]), before_):
        r = GetSite(sitenum, i)
        last[sitenum - 1] = last[sitenum - 1][0:28] + str(i + 1) + '\n'
        if sitenum == 3:
            for url in re.findall('(https://unsplash.com/photos/[a-zA-Z0-9-]+/download)', r.text): 
                photo.append(url)

        elif sitenum == 4:
            soup = BeautifulSoup(requests.get('https://akspic.ru/album/anime/3840x2160?' + s_last_1 + str(i), headers=headers).content, 'html.parser')
            con = soup.find_all("script", {'type' : 'application/ld+json'})
            for url in re.findall(r'(https://img[1-9].akspic.ru/originals/[1-9/]+\-[a-zA-Z_\-]*3840x2160.jpg)', str(con)):
                photo.append(url)
        
            soup = BeautifulSoup(requests.get('https://akspic.ru/search/аниме/1440x2960?' + s_last_1 + str(i), headers=headers).content, 'html.parser')
            con = soup.find_all("script", {'type' : 'application/ld+json'})
            for url in re.findall(r'(https://img[1-9].akspic.ru/originals/[1-9/]+\-[a-zA-Z_\-]*1440x2960.jpg)', str(con)):
                photo.append(url)

        elif sitenum == 1 or sitenum == 2:
            for url in re.findall('(https://unsplash.com/photos/[a-zA-Z0-9-]+/download\?ixid=[a-zA-Z0-9]+)', r.text): 
                photo.append(url)
        else:
            r = requests.get('https://wallhaven.cc/search?categories=100&purity=100&sorting=date_added&order=desc&' + s_last_1 + str(i), headers=headers)
            link = []
            soup = BeautifulSoup(r.content, 'html.parser')
            con = soup.find_all("figure", {'class' : 'thumb'})
            for url in re.findall(r'(https://wallhaven.cc/[a-z]/[a-z1-9-]+)', str(con)):
                link.append(url)

            for i in range(0, len(link)):
                r = requests.get(link[i], headers=headers)
                soup = BeautifulSoup(r.content, 'html.parser')
                con = soup.find_all("img", {'id' : 'wallpaper'})
                try:
                    photo.append(re.findall(r'(https://w.wallhaven.cc/full/[1-9a-z-]+/[a-z1-9-\-]+.jpg)', str(con))[0])
                except:
                    i += 1

    
    #записываем в файл скаченых страниц и сообщаем пользователю что ссылки собраны
    bot.send_message(message.chat.id, "Сбор " + str(len(photo)) + " сcылок закончен. Приступаю к скачиваюнию фотографий с " + str(len(photo)) + " страниц.")
    for i in range(0, len(last)):
        per.write(last[i])
    #записываем в стату скаченые фотографии
    stats = open('config/Stats.txt', 'r').readlines()
    stats[0] = str(int(stats[0]) + len(photo)) + '\n'
    per = open('config/Stats.txt', 'w')
    for i in range(0, len(stats)):
        per.write(str(stats[i]))
    return photo

def GetPhoto(message, bot, photo_link):
    #список фотографий имеено файлов
    photo = []
    #записываем в переменную класс sen_message
    ID_mes = bot.send_message(message.chat.id, "Скачано фото: 0")
    try:
        for i in range(0, len(photo_link)):
            try:
                #берем айди для лс с ботом чтобы назвать файлы
                id_p = open('config/IDPhotoNow.txt', "r").readlines()
                #называем файлы
                src = "photos/" + 'n0walls_' + id_p[0] + ".png"
                #записываем новое значение в айди
                open('config/IDPhotoNow.txt', "w").write(str(int(id_p[0]) + 1))
                #скачивание фото запись в папку и добавление в список
                r = requests.get(photo_link[i], allow_redirects=True)

                with open(src, 'wb') as new_file: new_file.write(r.content)

                photo.append(r.content)

                bot.edit_message_text(chat_id=message.chat.id, message_id=ID_mes.message_id, text="Скачано фото: " + str(len(photo)))

            except Exception as e:
                i += 1
                print('\nget_photo_1-1:')
                print(repr(e))

    except Exception as e:
        print('\nget_photo_1-2:')
        print(repr(e))

    return photo

def GetSite(sitenum, i):
    #для 3-го сайта другое выражение поэтому так
    if sitenum == 3: return requests.get(sites[sitenum - 1] + s_last_1 + str(i) + s_last_3)
    return requests.get(sites[sitenum - 1] + s_last_1 + str(i) + s_last_2)
