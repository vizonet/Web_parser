import re
import json
import time
import datetime

from utils import getSearch, getContent


start = datetime.datetime.now()
REQUEST_PERIOD = 0    # 1.5 сек - период между запросами в цикле

# сайт университета ТУСУР
link1 = "https://tusur.ru/ru/search?utf8=✓&parts_params%5Bsearch%5D%5Bq%5D={}"
link = "https://tusur.ru/ru/search?page={}&parts_params%5Bsearch%5D%5Bq%5D={}"

# файл результатов
resFile = "pages.json"
# файл поисковых запросов
searchFile = "search.txt"

# поисковые запросы
search = getSearch(searchFile)

# Поисковая фраза # пробелы между словами заменяются на +
SEARCH_GLOBAL = re.sub("[\s]+", " ", search[0].strip())
print(f"\nОсновной запрос: \"{SEARCH_GLOBAL}\"")
searchGlobal = re.sub("[\s]+", "+", SEARCH_GLOBAL)

# Поиск в результатах
SEARCH_STR = re.sub("[\s]+", " ", search[1].strip())
print(f"Поиск в результатах: \"{SEARCH_STR}\"\n")
searchStr = re.sub("[\s]+", "+", SEARCH_STR)

# число страниц результатов поискового запроса
num = 1
soup = getContent(link.format(num, searchGlobal))
pages = soup.findAll(class_="page")

if not pages:
    pages = [soup]
    pageNums = 1
    # print('Нет результатов поиска по основному запросу!')
    # exit(0)
else:
    pageNums = int(pages[-1].a.string)

print(f"Всего страниц: {pageNums}")

# постраничный парсинг
txt_list = []   # найденные конечные результаты
for pageNum in range(1, pageNums + 1):
    start = datetime.datetime.now()
    # запрос
    query = link.format(pageNum, searchGlobal)
    # разбор страницы
    html_a = getContent(query).select("[class$=search_results] > ul > li > h4 > a")  # .select("[class$=search_results] > ul > li > p") # .findAll("p", class_="search_results") - не работает
    html_p = getContent(query).select("[class$=search_results] > ul > li > p")
    # список ссылок
    for i in range(len(html_a)):
        txt = html_p[i].text
        url = html_a[i].get('href')
        if searchStr.lower() in txt.lower():
            txt_list.append({
                f"{pageNum}-{i+1}": txt,
                "url": url,
            })
            print(f"--> Найдено -> Page {pageNum} [{i+1}] ")

    time.sleep(REQUEST_PERIOD)
    end = datetime.datetime.now()
    print(f"Обработано -> Page {pageNum} за {end - start}")

cntRes = len(txt_list)
print(f"\nНайдено ссылок: {cntRes}")

# запись найденного списка в файл
with open(resFile, "w", encoding='utf-8') as file:
    json.dump(txt_list, file, ensure_ascii=False, indent=4)
    # if cntRes:
    print(f"Найденные ссылки сохранены в файле \"{resFile}\"")

# завершение
end = datetime.datetime.now()
duration = end - start
print(f"\nВремя работы программы: {duration}")
