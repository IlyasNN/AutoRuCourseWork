import requests
from bs4 import BeautifulSoup as bs
import csv
import time

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'
           }

GENDER = 'мужчиной'
# GENDER = 'девушкой'

BASE_URL = 'https://badoo.com/dating/russia/page-1/'


def parse_profile(url, headers):
    name = ''
    male = ''
    location = ''
    age = 0
    link = url
    aim = ''
    interests = []

    s = requests.Session()
    r = s.get(url, headers=headers)
    if r.status_code == 200:
        soup = bs(r.content, 'html.parser')
        title = soup.find('title').text
        titleElements = title.split(' | ')
        [name, male, age] = titleElements[0].split(', ')

        location = soup.find('div',
                             class_='profile-section qa-profile-section-location')
        location = location.find('div', class_='profile-section__view').text
        location = location.split('  ')[0]

        aim = soup.find('div', class_='profile-section qa-profile-section-iht')
        aim = aim.find('div', class_='profile-section__view').text

        try:
            interestsSrc = soup.find('div', class_='pills')
            interestsSrc = interestsSrc.find_all('div', class_='pills__item')
            for item in interestsSrc:
                interests.append(item.find('span', class_='pill__text').text)
        except Exception:
            interests = []

        return name, male, location, age, link, aim, interests

    else:
        print('ERROR')

    return aim


def parse_page(page_url, headers):
    base = 'https://badoo.com'
    s = requests.Session()
    r = s.get(page_url, headers=headers)
    if r.status_code == 200:
        soup = bs(r.content, 'html.parser')
        cells = soup.find_all('div', class_='users-list__cell')
        matches = []
        for cell in cells:
            a = cell.find('a', class_='user-card__link')
            link = base + a['href']
            name, male, location, age, link, aim, interests = parse_profile(link,
                                                                      headers)

            info = (name, male, location, age, link, aim, interests)
            with open('Badoo.csv', 'a') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(info)
                print('CSV written')

    next_button = base + soup.find('a',
                                   class_='react-button react-button--sm react-button--color-gray-dark react-button--transparent js-pages')[
        'href']
    if next_button is None:
        next_button = ''

    return next_button


def main():
    with open('Badoo.csv', 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(
            ['name', 'male', 'location', 'age', 'link', 'aim', 'interests'])

    url = BASE_URL
    next_button = '0'
    page = 1
    while True:
        if next_button == '':
            break
        else:
            print('Parsing page', page)
            next_button = parse_page(url, headers)
            # write_csv(matches)
            # all_matches.extend(matches)
            url = next_button
            page += 1


if __name__ == '__main__':
    main()
