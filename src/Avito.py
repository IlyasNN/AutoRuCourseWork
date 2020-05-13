import requests
import bs4


HEADERS = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'
           }

URL = 'https://avito.ru/nizhniy_novgorod/'


def getBlocks(text):
    soup = bs4.BeautifulSoup(text, 'lxml')
    # div.snippet-horizontal.item.item_table.clearfix.js-catalog-item-enum.item-with-contact.js-item-extended
    container = soup.find_all('div', class_='styles-root-2Jty7')
    for item in container:
        # self.parseBlock(item)
        print(item)
        print()


def parseBlock(self, item):
    pass


def main():
    s = requests.Session()
    r = s.get(URL, headers=HEADERS)
    getBlocks(r.text)
    print()

if __name__ == '__main__':
    main()
