import csv
import requests
from bs4 import BeautifulSoup
from lxml import etree
import random
import time

def scrape_restaurants(zip_codes, page_limit):
    rest_name = []
    links = []
    websites = []
    phone_numbers = []
    addresses = []
    IsClaimed = []
    foodTypes = []
    rates = []
    reviews = []
    Time = []

    for zip_code in zip_codes:
        page_number = 0

        while True:
            result = requests.get(f"https://www.yelp.com/search?find_desc=Restaurants&find_loc={zip_code}&start={page_number}")
            src = result.content
            soup = BeautifulSoup(src, 'lxml')

            if page_number >= page_limit:
                print(f"Reached page limit for zip code {zip_code}")
                break

            restaurants_names = soup.select('div > h3 > span > a', {'class': 'css-19v1rkv'})
            yelp = 'https://yelp.com'

            for i in range(len(restaurants_names)):
                rest_name.append(restaurants_names[i].text)
                links.append(yelp + restaurants_names[i].get('href'))

            page_number += 10
            print(f"Page Switched for zip code {zip_code}")
            # Random Delay between 3, 7
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

            website_xpath = "/html/body/yelp-react-root/div[1]/div[5]/div/div[1]/div[2]/aside/section[1]/div/div[1]/div/div[1]/p[2]/a"
            website = tree.xpath(website_xpath)
            websites.append(website[0].text if website else "None")

            address = soup.select("div > p.css-qyp8bo")
            addresses.append(address[0].text if address else "None")

            review = soup.select("span > a.css-19v1rkv")
            reviews.append(review[0].text if review else "None")

            foodType_xpath = "/html/body/yelp-react-root/div[1]/div[3]/div[1]/div[1]/div/div/span[3]/span[2]/a"
            foodType = tree.xpath(foodType_xpath)
            foodTypes.append(foodType[0].text if foodType else "None")


            claimed = soup.select("span.bullet--light__09f24__TY0D4")
            IsClaimed.append(claimed[0].text)

            rate_xpath = "/html/body/yelp-react-root/div[1]/div[3]/div[1]/div[1]/div/div/div[2]/div[2]/span[1]"
            rate = tree.xpath(rate_xpath)
            rates.append(rate[0].text if rate else "None")

            working_time_xpath = '//*[@id="location-and-hours"]/section/div[2]/div[2]/div/div/table/tbody'
            working_time = tree.xpath(working_time_xpath)
            # Convert the working time list to a string for each restaurant
            working_time_text = [','.join(timing.xpath('.//text()')) for timing in working_time]
            Time.append(working_time_text[0] if working_time_text else "None")


        except requests.exceptions.RequestException as e:
            print(f"Error fetching content from {link}: {e}")

        # Random Delay between 1, 5
        # delay_between_requests = random.uniform(1, 5)
        time.sleep(delay_between_requests)

    file_list = [rest_name, links, websites, phone_numbers, addresses, IsClaimed, foodTypes, rates, reviews, Time]
    exported = zip(*file_list)

    file_path = "/Users/abdulsalamhijazikelani/Desktop/output.csv"
    with open(file_path, "w") as output:
        writer = csv.writer(output)
        writer.writerow(["Names", "Links", "Websites", "Phone Numbers", "Addresses", "Is Claimed", "Food Type", "Rate", "Review", "Working Time"])
        writer.writerows(exported)

# List of zip codes...
zip_codes = [11201]

# 24 page for each zip code
page_limit = 10

scrape_restaurants(zip_codes, page_limit)