import csv

import requests
from bs4 import BeautifulSoup

PAGE = 'http://localhost:8000/auto_mpg.html'


def process_car_blocks(soup):
    car_blocks = soup.find_all('div', class_='car_block')
    print(car_blocks)
    rows = []
    for cb in car_blocks:
        str_name = cb.find('span', class_='car_name').text
        str_cylinders = cb.find('span', class_='cylinders').text
        cylinders = int(str_cylinders)
        assert cylinders > 0, f"Expected value to be positive {cylinders}"
        print(cylinders)
        str_weight = cb.find('span', class_='weight').text
        weight = int(str_weight.replace(',', ''))
        assert weight > 0, f"Expected value to be positive {weight}"
        str_from = cb.find('span', class_='from').text
        year, territory= str_from.strip('()').split(',')
        territory = territory.strip()
        acceleration = float(cb.find('span', class_='acceleration').text)
        mpg_str = cb.find('span', class_='mpg').text
        try:
            mpg = float(mpg_str.split(' ')[0])
            assert mpg > 7
        except ValueError:
            mpg = 'NULL'

        row = dict(name=str_name, cylinders=cylinders, weight=weight,
                   territory=territory, year=year, acceleration=acceleration,
                   mpg=mpg)
        rows.append(row)

    print(f"we have {len(rows)} of scraped data...")
    print(rows[0])
    print(rows[-1])
    write_csv(rows)


def write_csv(rows):
    with open('scraped_cars.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=rows[-1].keys())
        writer.writeheader()
        writer.writerows(rows)


if __name__ == '__main__':
    result = requests.get(PAGE)
    assert result.status_code == 200, f"Got status code {result.status_code} which is not a success"
    source = result.text
    soup = BeautifulSoup(source, 'html.parser')
    process_car_blocks(soup)
