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

page_number = 10
page_limit = 500

while True:
    # Use requests to fetch the rul
    result = requests.get(f"https://www.tripadvisor.com/RestaurantSearch-g60763-oa{page_number}-a_geobroaden.false-New_York_City_New_York.html#EATERY_LIST_CONTENTS")

    # Save page content
    src = result.content

    # Create soup object to parse content
    soup = BeautifulSoup(src, 'lxml')
    if (page_number >= page_limit):
        print("Last Page")
        break

    # Find element containing info we need
    restaurants_names = soup.select('div > span > a.Lwqic')
    print(restaurants_names)
    # yelp = 'https://yelp.com'

    # loop over returned lists to extract needed info into other lists
    for i in range(len(restaurants_names)):
        rest_name.append(restaurants_names[i].text)
        links.append(restaurants_names[i].get('href'))
    page_number += 30
    print("Page Switched")
    print(restaurants_names)
    delay_between_requests = random.uniform(3, 7)
    time.sleep(delay_between_requests)

#
# for link in links:
#     try:
#         result = requests.get(link, timeout=10)
#         src = result.content
#         tree = etree.HTML(src)
#         soup = BeautifulSoup(src, "lxml")
#
#         phone_number_xpath = "/html/body/yelp-react-root/div[1]/div[5]/div/div[1]/div[2]/aside/section[1]/div/div[2]/div/div[1]/p[contains(@class, ' css-1p9ibgf')]"
#         phone_number_element = tree.xpath(phone_number_xpath)
#         phone_numbers.append(phone_number_element[0].text if phone_number_element else "None")
#
#         website = soup.select("div > p > a.css-1idmmu3")
#         websites.append(website[0].text if website else "None")
#
#         address = soup.select("div > p.css-qyp8bo")
#         addresses.append(address[0].text if address else "None")
#
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching content from {link}: {e}")
#
#     delay_between_requests = random.uniform(1, 5)
#     time.sleep(delay_between_requests)
#
#
# # Combine the lists using zip (no need for zip_longest)
# file_list = [rest_name, links, websites, phone_numbers, addresses]  # Change the order to match the header row
# exported = zip(*file_list)
#
# file_path = "/Users/abdulsalamhijazikelani/Desktop/untitled-folder/output-file.csv"
# with open(file_path, "w") as output:
#     writer = csv.writer(output)
#     writer.writerow(["Names", "Links", "Websites", "Phone Numbers", "Addresses"])
#     writer.writerows(exported)