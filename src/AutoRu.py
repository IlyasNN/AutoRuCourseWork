import requests
import csv

# Заголовки страницы
HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Content-Length': '137',
    'content-type': 'application/json',
    'Cookie': '_csrf_token=1c0ed592ec162073ac34d79ce511f0e50d195f763abd8c24; autoru_sid=a%3Ag5e3b198b299o5jhpv6nlk0ro4daqbpf.fa3630dbc880ea80147c661111fb3270%7C1580931467355.604800.8HnYnADZ6dSuzP1gctE0Fw.cd59AHgDSjoJxSYHCHfDUoj-f2orbR5pKj6U0ddu1G4; autoruuid=g5e3b198b299o5jhpv6nlk0ro4daqbpf.fa3630dbc880ea80147c661111fb3270; suid=48a075680eac323f3f9ad5304157467a.bc50c5bde34519f174ccdba0bd791787; from_lifetime=1580933172327; from=yandex; X-Vertis-DC=myt; crookie=bp+bI7U7P7sm6q0mpUwAgWZrbzx3jePMKp8OPHqMwu9FdPseXCTs3bUqyAjp1fRRTDJ9Z5RZEdQLKToDLIpc7dWxb90=; cmtchd=MTU4MDkzMTQ3MjU0NQ==; yandexuid=1758388111580931457; bltsr=1; navigation_promo_seen-recalls=true',
    'Host': 'auto.ru',
    'origin': 'https://auto.ru',
    'Referer': 'https://auto.ru/ryazan/cars/mercedes/all/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
    'x-client-app-version': '202002.03.092255',
    'x-client-date': '1580933207763',
    'x-csrf-token': '1c0ed592ec162073ac34d79ce511f0e50d195f763abd8c24',
    'x-page-request-id': '60142cd4f0c0edf51f96fd0134c6f02a',
    'x-requested-with': 'fetch'
}

# URL на который будет отправлен запрос
URL = 'https://auto.ru/-/ajax/desktop/listing/'

# Параметры запроса
PARAMS = {
    # 'catalog_filter': [{"mark": "VAZ"}],
    'section': "all",
    'category': "cars",
    'sort': "fresh_relevance_1-desc",
}


def parse_page(page):
    PARAMS['page'] = page

    response = requests.post(URL, json=PARAMS,
                             headers=HEADERS)  # Делаем post запрос на url
    data = response.json()[
        'offers']  # Переменная data хранит полученные объявления

    img_url = []  # Словарь в котором будут все картинки

    i = 0  # Переменная для перехода по объявлениям
    while i <= len(
            data) - 1:  # len(data)-1 это количество пришедших объявлений

        # Марка автомобиля
        try:
            Mark_info = str(
                data[i]['vehicle_info']['mark_info']['name'])
        except:
            Mark_info = 'NaN'

        # Модель автомобиля
        try:
            Model_info = str(
                data[i]['vehicle_info']['model_info']['name'])
        except:
            Model_info = 'NaN'

        # Год выпуска автомобиля
        try:
            Year = str(data[i]['documents']['year'])
        except:
            Year = 'NaN'

        # Регион, в котором находится автомобиль
        try:
            Region = str(
                data[i]['seller']['location']['region_info']['name'])
        except:
            Region = 'NaN'

        # Всё ли в порядке с Vin номером
        try:
            Vin_resolution = str(data[i]['documents']['vin_resolution'])
            if Vin_resolution == 'OK':
                Vin_resolution = True
            elif Vin_resolution == 'ERROR':
                Vin_resolution = False
            else:
                Vin_resolution = 'NaN'
        except:
            Vin_resolution = 'NaN'

        # Пробег автомобиля
        try:
            Mileage = str(data[i]['state']['mileage'])
        except:
            Mileage = 'NaN'

        # Мощность
        try:
            Horse_power = str(data[i]['owner_expenses']['horse_power'])
        except:
            Horse_power = 'NaN'

        # Колличество владельцев автомобиля
        try:
            Owners_number = str(data[i]['documents']['owners_number'])
        except:
            Owners_number = 'NaN'

        # Тип автомобиля
        try:
            Body_type = str(
                data[i]['vehicle_info']['configuration']['body_type'])
        except:
            Body_type = 'NaN'

        # PTS автомобиля
        try:
            PTS = str(data[i]['documents']['pts'])
            if PTS == 'ORIGINAL':
                PTS = True
            else:
                PTS = False
        except:
            PTS = 'NaN'

        # Цвет автомобиля (возвращается в формате hex)
        try:
            Color_hex = str(data[i]['color_hex'])
        except:
            Color_hex = 'NaN'

        # С салона ли машина или нет
        try:
            Salon = str(data[i]['salon']['is_official'])
        except:
            Salon = 'NaN'

        # Количество дверей у автомобиля
        try:
            Count_doors = str(
                data[i]['vehicle_info']['configuration']['doors_count'])
        except:
            Count_doors = 'NaN'

        # Класс автомобиля
        try:
            Auto_class = str(
                data[i]['vehicle_info']['configuration']['auto_class'])
        except:
            Auto_class = 'NaN'

        # Объем багажника автомобиля
        try:
            Trunk_volume_min = str(
                data[i]['vehicle_info']['configuration']['trunk_volume_min'])
        except:
            Trunk_volume_min = 'NaN'

        # Цена в рублях, евро и долларах
        try:
            Price_rub = str(data[i]['price_info']['RUR'])
        except:
            Price_rub = 'NaN'

        # Картинки автомобиля
        # Возвращается несколько фото, мы их добавляем в словарь img_url
        for img in data[i]['state']['image_urls']:
            img_url.append(img['sizes']['1200x900'])

        # Информация об автомобиле
        try:
            Ik_summary = str(data[i]['lk_summary'])
        except:
            Ik_summary = 'NaN'

        link_img = ''  # Переменная для ссылок
        for link_img_0 in img_url:  # Перебираем ссылки из словаря img_url, и записываем их в одну переменную текстом
            link_img += str(link_img_0) + '\n'

        with open('autoRu.csv', 'a') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow((
                Mark_info,
                Model_info,
                Year,
                Region,
                Vin_resolution,
                Mileage,
                Owners_number,
                Body_type,
                PTS,
                Color_hex,
                Salon,
                Count_doors,
                Auto_class,
                Trunk_volume_min,
                Price_rub
            ))
            print('CSV written')

        i += 1  # Увеличиваем переменную перехода по объявлениям на 1

    return len(data)


def main():
    number_of_parsed = 0

    with open('autoRu.csv', 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(
            ['Mark_info',
             'Model_info',
             'Year',
             'Region',
             'Vin_resolution',
             'Mileage',
             'Owners_number',
             'Body_type',
             'PTS',
             'Color_hex',
             'Salon',
             'Count_doors',
             'Auto_class',
             'Trunk_volume_min',
             'Price_rub'
             ])

    for page in range(0, 100):
        number_of_parsed += parse_page(page)
        print('Page: ' + str(page))

    print('Successfully parsed: ')
    print(number_of_parsed)


if __name__ == '__main__':
    main()
