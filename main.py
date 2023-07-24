import csv
import requests
from bs4 import BeautifulSoup
from itertools import zip_longest
from lxml import etree
import random
import time

rest_name = []
links = []
websites = []
phone_numbers = []
addresses = []

page_number = 0
page_limit = 240
zip_codes = [11201, 11203, 11204, 11205, 11206, 11207, 11208, 11209, 11210, 11211,
                11212, 11213, 11214, 11215, 11216, 11217, 11218, 11219, 11220, 11221,
                11222, 11223, 11224, 11225, 11226, 11228, 11229, 11230, 11231, 11232,
                11233, 11234, 11235, 11236, 11237, 11238, 11239 ]

while True:
    # Use requests to fetch the rul
    result = requests.get(f"https://www.yelp.com/search?find_desc=Restaurants&find_loc={zip_codes}&start={page_number}")

    # Save page content
    src = result.content

    # Create soup object to parse content
    soup = BeautifulSoup(src, 'lxml')
    if (page_number >= page_limit):
        print("Last Page")
        break

    # Find element containing info we need
    restaurants_names = soup.select('div > h3 > span > a', {'class': 'css-19v1rkv'})
    yelp = 'https://yelp.com'

    # loop over returned lists to extract needed info into other lists
    for i in range(len(restaurants_names)):
        rest_name.append(restaurants_names[i].text)
        links.append(yelp + restaurants_names[i].get('href'))
    page_number += 10
    print("Page Switched")
    delay_between_requests = random.uniform(3, 7)
    time.sleep(delay_between_requests)


for link in links:
    try:
        result = requests.get(link, timeout=10)
        src = result.content
        tree = etree.HTML(src)
        soup = BeautifulSoup(src, "lxml")

        phone_number_xpath = "/html/body/yelp-react-root/div[1]/div[5]/div/div[1]/div[2]/aside/section[1]/div/div[2]/div/div[1]/p[contains(@class, ' css-1p9ibgf')]"
        phone_number_element = tree.xpath(phone_number_xpath)
        phone_numbers.append(phone_number_element[0].text if phone_number_element else "None")

        website = soup.select("div > p > a.css-1idmmu3")
        websites.append(website[0].text if website else "None")

        address = soup.select("div > p.css-qyp8bo")
        addresses.append(address[0].text if address else "None")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {link}: {e}")

    delay_between_requests = random.uniform(1, 5)
    time.sleep(delay_between_requests)


# Combine the lists using zip (no need for zip_longest)
file_list = [rest_name, links, websites, phone_numbers, addresses]  # Change the order to match the header row
exported = zip(*file_list)

file_path = "/Users/abdulsalamhijazikelani/Desktop/untitled-folder/output-file.csv"
with open(file_path, "w") as output:
    writer = csv.writer(output)
    writer.writerow(["Names", "Links", "Websites", "Phone Numbers", "Addresses"])
    writer.writerows(exported)