import re
import requests
from bs4 import BeautifulSoup


def getSearch(searchFile):
    # возвращает 2 запроса поиска
    mark = '[#'  # метка запроса, комментарий
    search = []  # список запросов (основного на странице поиска и доп. в найденных результатах)

    # чтение файла запросов
    with open(searchFile, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # обработка строк, запрос может быть на нескольких строках
    string = ''
    for line in lines:
        if mark in line:  # пропуск метки
            flag = True
            # очередной запрос
            # r = re.search("^[0-9]+", f"{line.lstrip(mark)}")

        else:   # продолжение запроса на след. строке
            string += line
            flag = False

        # запись собранной фразы
        if (flag and string) or (line == lines[-1] and string):  # с учетом конца файла
            search.append(string)
            string = ''

    return search


def getContent(url):
    # возвращает объект контента по заданной ссылке
    return BeautifulSoup(requests.get(url).content, "html.parser")
