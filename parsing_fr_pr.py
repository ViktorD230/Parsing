import requests
from bs4 import BeautifulSoup
import json


#first parth

persons_url_list = []

for i in range (0, 360, 20):
    url = f"https://www.senat.fr/vos-senateurs/recherche-de-senateurs/recherche-avancee-de-senateurs?limit=20&noFilterSet=true&offset={i}"

    q = requests.get(url)
    result = q.content

    soup = BeautifulSoup(result, "lxml")
    persons = soup.find_all(class_="card-title stretched-link")

    for person in persons:
        person_page_url = person.get("href")
        persons_url_list.append(person_page_url)

with open('persons_url_list.txt', 'a') as file:
    for line in persons_url_list:
        file.write(f'{line}\n')


#second parth

with open('persons_url_list.txt') as file:
    lines = [line.strip() for line in file.readlines()]

data_dict = []
count = 0

for line in lines:
    line = line.strip()
    try:
        q = requests.get(line)
        result = q.content

        soup = BeautifulSoup(result, 'lxml')
        person = soup.find(class_="col-12 order-1 col-md-7 order-md-0").find('h1').text
        person_company = soup.find(class_="col-12 order-1 col-md-7 order-md-0").find('p').text.strip()
        full_name = person + person_company.strip()

        social_networks = soup.find_all(class_="")

        social_networks_urls = []
        for item in social_networks:
            url = item.get('href')
            if url and url.startswith(("https://twitter.com/", "https://www.facebook.com/",
                                       "https://www.youtube.com/", "https://www.tiktok.com/")):
                social_networks_urls.append(url)

        data = {
            "person_name": person,
            "person_company": person_company,
            "social_networks": social_networks_urls
        }

        count += 1
        print(f"#{count}: {line} is done!")

        data_dict.append(data)
    except requests.exceptions.MissingSchema:
        print(f"Ошибка: Неправильный URL-адрес '{line}'. Убедитесь, что вы предоставили правильную схему (например, 'http://' или 'https://').")
    except requests.exceptions.RequestException as e:
        print("Ошибка при выполнении запроса:", e)

with open('data.json', "w") as json_file:
    json.dump(data_dict, json_file, indent=4)

