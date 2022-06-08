import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service


CHROME_DRIVER_PATH = "C:\Development\chromedriver.exe"
WEBSITE_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdKnDjijZXREMLZ3QEzEcU8Rmb2aZTCGLJu0Rz6F46IGnqJYg/viewform?usp=sf_link"

HEADERS = {
    "Accept-Language": "en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 "
                  "Safari/537.36 ",
}

response = requests.get(url=WEBSITE_URL, headers=HEADERS)

soup = BeautifulSoup(response.text, "html.parser")

# all_price_elements = soup.select(".list-card-details li")
# all_prices = [price.get_text().split("+")[0]]
# for price in all_prices:
#     print(price)

all_link_elements = soup.select(".list-card-top a")
# print(all_link_elements)
all_links = []
for link in all_link_elements:
    href = link["href"]
    # print(href)
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)
    print(all_links)


all_address_elements = soup.select(".list-card-addr")
# print(all_address_elements)
all_address = []
for address in all_address_elements:
    all_address = address.get_text().split(" | ")[-1]
    print(all_address)

all_price_elements = soup.select(".list-card-price")
all_price = []
for price in all_price_elements:
    all_price = price.get_text().split("+")[0]
    print(all_price)

s = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=s)
driver.maximize_window()

for n in range(len(all_links)):
    driver.get(GOOGLE_FORM_URL)
    time.sleep(3)

    addresses = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prices = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    links = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    addresses.send_keys(all_address[n])
    prices.send_keys(all_price[n])
    links.send_keys(all_links[n])
    submit.click()

    time.sleep(50000)

# driver.quit()