from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
import csv


options = Options()
# Запуск браузера с развернутым экраном
options.add_argument('start-maximized')
# Будем использовать браузер Chrom
driver = webdriver.Chrome(options=options)
# Открываем ссылку
driver.get('https://www.wildberries.ru')
time.sleep(4)

wait = WebDriverWait(driver, 10)
# Ищем строку поиска
input = wait.until(EC.presence_of_element_located((By.ID, "searchInput")))
# Вводим фразу поиска и нажимаем Enter
input.send_keys('книги машинное обучение')
input.send_keys(Keys.ENTER)

# Прокручиваем страницу и записываем все ссылки на книги,
# если есть кнопка "далее" - нажимаем её или выходим из цикла
while True:
    # Количество книг на странице
    count = None

    while True:
        time.sleep(4)
        # Ожидаем появление объекта (html код) карточек товара
        cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[@id]')))

        # Выходим из цикла, если при прокрутке страницы, количество товаров не меняется
        if len(cards) == count:
            break

        # Вычисляем сколько карточек товара на странице
        count = len(cards)

        # Прокручиваем страницу выполняя JAVA Script
        driver.execute_script('window.scrollBy(0, 1800)')
        time.sleep(2)

    # На полностью загруженной странице соберём информацию
    url_list = [card.find_element(By.XPATH, './div/a').get_attribute('href') for card in cards]

    # Проверяем есть ли кнопка next и кликаем три раза
    try:
        if click_count < 2:  # Проверяем счетчик кликов
            next = driver.find_element(By.CLASS_NAME, 'pagination-next')
            next.click()
            click_count += 1  # Увеличиваем счетчик
            time.sleep(2)  # Добавляем небольшую задержку
        else:
            break  # Выходим из основного цикла после 3 кликов
    except Exception:
        break

print(f'Всего получено: {len(url_list)} ссылок на книги')

# Заходим на каждую страницу найденных книг и парсим её
driver2 = webdriver.Chrome(options=options)
wait2 = WebDriverWait(driver2, 30)
# Создаем заголовок для CSV
fieldnames = ['name', 'price', 'brend', 'url', 'article', 'author', 'genre', 'language', 'year', 'cover']

# Основной цикл парсинга
books_list = []
for url_item in url_list:
    books_dict = {}

    driver2.get(url_item)

    # Заносим название книги
    books_dict['name'] = wait2.until(EC.presence_of_element_located((By.XPATH, "//h1"))).text

    # Заносим цену книги
    price = wait2.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'price-block__wallet-price')))
    try:
        books_dict['price'] = float(re.sub(r'[^\d.]+', '', price[1].text))
    except Exception:
        books_dict['price'] = None

    # Заносим издательство
    books_dict['brend'] = wait2.until(
        EC.presence_of_element_located((By.CLASS_NAME, "product-page__header-brand"))).text

    # Заносим URL
    books_dict['url'] = url_item

    # Обрабатываем табличные данные
    labels = wait2.until(EC.presence_of_all_elements_located((By.XPATH, '//th')))
    params = wait2.until(EC.presence_of_all_elements_located((By.XPATH, '//td')))
    description = {label.text: param.text for label, param in zip(labels, params)}

    fields = {'Артикул': 'article', 'Автор': 'author', 'Жанры/тематика': 'genre', 'Языки': 'language',
              'Год выпуска': 'year', 'Обложка': 'cover'}

    for label, field in fields.items():
        books_dict[field] = description.get(label)

    books_list.append(books_dict)

# Сохраняем данные в CSV с использованием DictWriter
with open('data.csv', 'w', newline='', encoding='Windows-1251') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()  # Автоматически записывает заголовок
    writer.writerows(books_list)