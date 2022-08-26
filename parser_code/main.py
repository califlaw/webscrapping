import requests
from bs4 import BeautifulSoup
import csv


# To scrap a website I need a requests and bs4 libraries

# To make my webscrapper working for all pages I decided to do that with function: URL will be inputted and then all
# code is going to work with it

def parser():
    counter = 0
    while True:
        ask = input("\nWould you like to webscrape the website? Y/n: ").lower()
        if ask == "y":
            webscrapper()
            reask = input("Another webpage?: Y/n: ").lower()
            counter += 1
            if reask == 'y':
                webscrapper()
                counter += 1
            else:
                print(f"Webscrapper done. You have written information for {counter} times.")
                break
        else:
            print("See you next time!")
            print(f"You have written information for {counter} times")
            break


# Initial webscrapper
def webscrapper():
    url = input("Put the link here: ")

    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/103.0.0.0 Safari/537.36 '}
    r = requests.get(url, headers=headers)
    src = r.text

    # Once I wrote the index.html to my project I can open it up and work with it. The code where it was written in
    # writing_file.py

    with open('parser_code/index.html', 'r') as f:
        src = f.read()

    soup = BeautifulSoup(src, 'html.parser')
    finder = soup.find_all('div', class_='item product_listbox oh')
    phones = []

    # I need phone names, description and price so let's take only them.
    for i in finder:
        phones.append({
            'Names': i.find('div', class_='listbox_title oh').get_text(strip=True),
            'Info': i.find('div', class_='product_text pull-left').get_text(strip=True),
            'Price': i.find('div', class_='listbox_price text-center').get_text(strip=True)
        })

        # Here is the writing to csv is going, "Цена" - Price, "Инфо" - "Info", "Цена" - "Price". Since I was doing
        # it for my local client, the columns' name should be in Russian. Once I name the columns I should comment it
        # not to ovewrite it.

    with open('saved_files/data.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(
            ("Цена",
             "Инфо",
             "Цена"
             )
        )

        # Here is I am looping through the "finder" and filling my csv file.

    for i in range(len(phones)):
        price = phones[i]['Price']
        nam = phones[i]['Names']
        inf = phones[i]['Info']
        with open('saved_files/data.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(
                (price,
                 nam,
                 inf
                 )
            )

    print(
        '\nWebscrapping done successfully and info was written in data.csv in saved_files directory. Put another '
        'website page from kivano.kg to parse more')


if __name__ == "__main__":
    parser()
