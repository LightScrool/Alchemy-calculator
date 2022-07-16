from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as BS
import time

data = []
recipes_to_track = []

with open('recipes to track.txt', 'r', encoding='utf-8') as file:
    for line in file.readlines():
        line = line.replace("\n", "")
        recipes_to_track.append(f'[{line}]')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
link = 'https://theunderminejournal.com/#eu/gordunni/category/alchemy'
driver.get(link)
time.sleep(2)  # Нужно дождаться, пока JavaScript на сайте загрузит всю информацию, времени может быть недостаточно
generated_html = driver.page_source
soup = BS(generated_html, 'html.parser')
driver.quit()

tables = soup.select('.category-items')
for table in tables:
    for tr in table.find_all('tr'):
        if (tr.select('.name') != []) and (tr.select('.sortable') == []):  # Отбрасываем строки-заголовки
            name = tr.select('.name')[0].text
            price = tr.select('.price')
            if name in recipes_to_track:
                data.append({
                    'name': name[1:-1],
                    'price': price[0].text,
                    'k': float(price[2].text) / float(price[0].text)
                })

data.sort(key=lambda x: x['k'])

for item in data:
    print(f'{item["name"]} - {round(item["k"], 2)} ({item["price"]})')

input('-------------------------------------')
