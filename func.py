# -*- coding: utf-8 -*-
def DesktopMobile(sizePhoto):
    #принимает строку примерно: (4000х5000) такого вида
    #с помощью разбиения получаем числа и возвращем тип уствойства под которое подходит фото
    width = int(sizePhoto[1:5])
    height = int(sizePhoto[6:10])

    if width > height: return "#desktop"
    else: return "#phone"

def Stats(added, line):
    stats = open('config/Stats.txt', 'r').readlines()
    stats[line] = str(int(stats[line]) + added) + '\n'
    per = open('config/Stats.txt', 'w')
    for i in range(0, len(stats)): 
        per.write(str(stats[i]))