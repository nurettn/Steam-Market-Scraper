import time
import csv
import re
import json
import urllib
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from fake_useragent import UserAgent

from Discord import Discord
from CurrencyExchanger import convertPrice
from Common import Common

delay_time = 25
item_name = ""
item_normalPrice = ""
item_salePrice = ""
item_count = ""
item_link = ""


def run():
    driver = Common.getDriver()
    with open("Items.csv", 'r', encoding="utf-8") as readFile:
        items = csv.reader(readFile)
        for item in items:
            item_name = item[0]
            item_normalPrice = item[1]
            item_salePrice = item[2]
            item_count = item[3]
            item_link = item[4]
            Common.sendLog("info", item[0] + " analysis has begun.")
            # driver.get(item_link+"?filter=sticker")
            driver.get(item_link)
            if "Souvenir" in item_name:
                continue
            time.sleep(delay_time)
            if Common.isListContainItem(driver) is False:
                continue
            Common.collapsePage(driver, 20)
            with open("page.html", "w", encoding="utf-8") as write_page:
                write_page.write(driver.page_source)
            with open("page.html", "r", encoding="utf-8") as read_page:
                response = read_page.read()
                page_soup = soup(response, "html.parser")
                searchResultsRows = page_soup.find("div", {"id": "searchResultsRows"})
                containers = searchResultsRows.find_all(attrs={"class": "market_listing_row"})
                for container in containers:
                    name_block = container.find("div", {"class": "market_listing_item_name_block"})
                    item_name = name_block.find("span", {"class": "market_listing_item_name"}).text

                    price_block = container.find("div", {"class": "market_listing_price_listings_block"})
                    price_block = price_block.find("span", {"class": "market_table_value"})
                    price_with_fee = re.sub("\s\s+", "", price_block.find(
                        attrs={"class": "market_listing_price market_listing_price_with_fee"}).text)
                    publisher_fee_only = re.sub("\s\s+", "", price_block.find(
                        attrs={"class": "market_listing_price market_listing_price_with_publisher_fee_only"}).text)
                    price_without_fee = re.sub("\s\s+", "", price_block.find(
                        attrs={"class": "market_listing_price market_listing_price_without_fee"}).text)

                    itemId = name_block.find('span').get("id")
                    js2 = re.search(
                        'CreateItemHoverFromContainer\( g_rgAssets, \'' + itemId + '\', 730, \'2\', (.*?), 1 \);',
                        response)
                    if js2 is None:
                        continue
                    itemId = js2.group(1).replace("'", "")

                    # Here we start to read the stickers
                    js = re.search('var g_rgAssets = (.*?}}});', response)
                    dic = json.loads(js.group(1))
                    for i, item in enumerate(dic['730']['2'][itemId]['descriptions']):
                        t1 = re.search('<br>Sticker:(.*?)</center>', str(item))
                        if isinstance(t1, re.Match):
                            stickers = re.search('<br>Sticker:(.*?)</center>',
                                                 str(dic['730']['2'][itemId]['descriptions'][i])).group(1)
                            # print(stickers)
                            ItemAnalys(item_name, price_with_fee, publisher_fee_only, price_without_fee, stickers,
                                       item_link, item_count)


def ItemAnalys(item_name, price_with_fee, publisher_fee_only, price_without_fee, stickers, item_link, item_count):
    stickersSplit = stickers.strip().split(",")
    if len(stickersSplit) < 3:
        return
    message = " **     Item Found      **\n"
    message += "**Item Name: **" + item_name + "\n"
    message += "**Item Count: **" + item_count + "\n"
    message += "**Price 1 (Steam+Valve): **" + convertPrice(price_with_fee, 'USD') + "\n"
    message += "**Price 2 (Valve): **" + convertPrice(publisher_fee_only, 'USD') + "\n"
    message += "**Price 3 (Tahsil): **" + convertPrice(price_without_fee, 'USD') + "\n"
    # sum_sticker_price = 0
    for i, sticker in enumerate(stickersSplit):
        message += "**Sticker " + str(i + 1) + ": **" + sticker + "\n"
    message += "**Link: ** <" + item_link + "> \n"
    message += "**Filter Link Stickers: ** <" + item_link + "?filter=sticker" + "> \n"
    message += "**Filter Link Stickers with Detail: ** <" + item_link + "?filter=" + urllib.parse.quote_plus(
        stickers) + "> \n"
    message += "**Keywords: **" + stickers + "\n"
    # message+="Keywords:"+stickers+"\n"
    Discord.Sender(message)


def getStickerwithPrice(sticker):
    found = False
    with open("Sticker.csv", 'r', encoding="utf-8") as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            sticker_name = row[0]
            if sticker_name == sticker:
                found = True
                return convertPrice(row[1], 'USD')
        # print("Name: {0}. Price {1}".format(sticker_name,sticker_price))
        if found is False:
            print("Sticker not found: " + sticker_name)
            Common.sendLog("info", sticker_name + "Not found")
