from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

def parse_description(desc):
    result = {}
    
    # Объём - число перед "куб. см"
    volume = re.search(r'(\d+)\s*куб\.?\s*см', desc)
    result['volume'] = volume.group(1) if volume else None
    
    # Пробег - число перед "км"
    distance = re.search(r'(\d[\d\s]*)\s*км', desc)
    result['distance'] = distance.group(1) if distance else None
    
    # Топливо
    if 'бензин' in desc:
        result['fuel'] = 'бензин'
    elif 'электро' in desc:
        result['fuel'] = 'электро'
    else:
        result['fuel'] = None
    
    # Тип двигателя
    if '4-тактный' in desc:
        result['engine_type'] = '4-тактный'
    elif '2-тактный' in desc:
        result['engine_type'] = '2-тактный'
    else:
        result['engine_type'] = None
        
    return result


motos = []
for i in range(1,101):

    page = requests.get(f'https://auto.drom.ru/moto/motorcycle/all/page{i}/').text

    soup = BeautifulSoup(page, 'lxml')


    moto_page = soup.find_all('div', class_="css-1f68fiz ea1vuk60")

    for motocycle in moto_page:    
        try:
            name = motocycle.find('h3', class_='css-16kqa8y efwtv890').text
            name, year = name.split(', ')
            year = int(year)
            moto_type = motocycle.find('div', class_='css-1hd50jd e3f4v4l0').text
            description = motocycle.find('div', class_='css-1fe6w6s e162wx9x0').text
            price = motocycle.find('div', class_='_1wx3rbx4').text
            place = motocycle.find('span', class_='css-1488ad e162wx9x0').text
        except AttributeError as e:
            print(f'мот на странице {i} не в продаже')
            continue

        mot ={
            'name': name,
            'year': year,
            'moto_type': moto_type,
            'description': description,
            'place': place,
            'price': price
        }
        motos.append(mot)
    



df = pd.DataFrame(motos)
df['parsed'] = df['description'].apply(parse_description)
df = pd.concat([df, df['parsed'].apply(pd.Series)], axis=1)
df = df.dropna(subset=['volume', 'distance', 'fuel', 'engine_type'])
df['price'] = df['price'].str.replace('\xa0', '').str.replace('₽', '').str.strip().astype(int)
df['distance'] = df['distance'].str.replace(' ', '').str.strip().astype(int)
df= df[['name', 'year', 'moto_type', 'place', 'price', 'volume', 'distance', 'fuel', 'engine_type']]    
df.to_csv('./data/motos.csv', index=False)
