import requests
from bs4 import BeautifulSoup

PAGE = 'http://localhost:8000/auto_mpg.html'


def process_car_blocks(soup):
    car_blocks = soup.find_all('div', class_='car_block')
    for cb in car_blocks:
        str_name = cb.find('span', class_='car_name').text


if __name__ == '__main__':
    result = requests.get(PAGE)
    assert result.status_code == 200, f"Got status code {result.status_code} which is not a success"
    source = result.text
    soup = BeautifulSoup(source, 'html.parser')
    process_car_blocks(soup)
