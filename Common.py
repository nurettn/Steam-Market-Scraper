from bs4 import BeautifulSoup as soup
import csv
import time
from fake_useragent import UserAgent
from selenium import webdriver
from Discord import Discord
import logging


class Common(object):
    @staticmethod
    def printToFile(file_name, item_name, item_normalPrice, item_salePrice, item_count, item_link):
        try:
            lines = list()
            with open(file_name, 'r', encoding="utf-8") as readFile:
                reader = csv.reader(readFile)
                for row in reader:
                    lines.append(row)
                    for field in row:
                        if field == item_name:
                            lines.remove(row)

            with open(file_name, 'w', newline='', encoding="utf-8") as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(lines)

            with open(file_name, 'a+', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([item_name, item_normalPrice, item_salePrice, item_count, item_link])
        except Exception as e:
            Common.sendLog("critical", e)

    @staticmethod
    def getItemName(container):
        try:
            name_block = container.find("div", {"class": "market_listing_item_name_block"})
            item_name = name_block.find("span", {"class": "market_listing_item_name"}).text
            if "Sticker | " in item_name:
                item_name = item_name.replace("Sticker | ", "")
            return item_name
        except Exception as e:
            Common.sendLog("critical", e)

    @staticmethod
    def getNormalPrice(container):
        try:
            price_block = container.find("div", {"class": "market_listing_right_cell market_listing_their_price"})
            item_price = price_block.find("span", {"class": "market_table_value normal_price"})
            normal_price = item_price.find("span", {"class": "normal_price"}).text
            return normal_price
        except Exception as e:
            Common.sendLog("critical", e)

    @staticmethod
    def getSalePrice(container):
        try:
            price_block = container.find("div", {"class": "market_listing_right_cell market_listing_their_price"})
            item_price = price_block.find("span", {"class": "market_table_value normal_price"})
            sales_price = item_price.find("span", {"class": "sale_price"}).text
            return sales_price
        except Exception as e:
            Common.sendLog("critical", e)

    @staticmethod
    def getItemCount(container):
        try:
            count_block = container.find("div", {"class": "market_listing_price_listings_block"})
            item_count = count_block.find("span", {"class": "market_listing_num_listings_qty"}).text
            item_count = item_count.replace(',', '')
            item_count = int(item_count)
            return item_count
        except Exception as e:
            Common.sendLog("critical", e)

    @staticmethod
    def getItemLink(container):
        try:
            return container.attrs['href']
        except Exception as e:
            Common.sendLog("critical", e)

    @staticmethod
    def collapsePage(driver, size):
        try:
            driver.execute_script("g_oSearchResults.m_cPageSize = " + str(size) + ";")
            driver.execute_script("g_oSearchResults.m_cMaxPages = Math.ceil(g_oSearchResults.m_cTotalCount / 100);")
            driver.execute_script("g_oSearchResults.GoToPage(g_oSearchResults.m_iCurrentPage, true);")
        except Exception as e:
            Common.sendLog("critical", e)

    @staticmethod
    def NextPage(driver):
        try:
            driver.execute_script("g_oSearchResults.NextPage()")
        except Exception as e:
            Common.sendLog("critical", e)

    @staticmethod
    def isListContainItem(driver):
        try:
            response = driver.page_source
            page_soup = soup(response, "html.parser")
            market_listing_table_message = page_soup.find("div", {"class": "market_listing_table_message"})
            if (market_listing_table_message is None):
                return True
            else:
                return False
        except Exception as e:
            Common.sendLog("critical", e)

    @staticmethod
    def getDriver():
        try:
            user_agent = UserAgent()
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('user-agent={0}'.format(user_agent.random))
            driver = webdriver.Chrome(chrome_options=chrome_options)
            return driver
        except Exception as e:
            Common.sendLog("critical", e)

    @staticmethod
    def getContainers(driver):
        try:
            response = driver.page_source
            page_soup = soup(response, "html.parser")
            searchResultsRows = page_soup.find("div", {"id": "searchResultsRows"})
            containers = searchResultsRows.find_all("a", {"class": "market_listing_row_link"})
            return containers
        except Exception as e:
            Common.sendLog("critical", e)

    @staticmethod
    def getcMaxPages(driver):
        try:
            return driver.execute_script("return g_oSearchResults.m_cMaxPages")
        except Exception as e:
            Common.sendLog("critical", e)

    @staticmethod
    def getiCurrentPage(driver):
        try:
            return driver.execute_script("return g_oSearchResults.m_iCurrentPage") + 1
        except Exception as e:
            Common.sendLog("critical", e)

    @staticmethod
    def sendLog(level, message):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%d-%m-%Y %H:%M:%S',
                            filename='trade.log',
                            filemode='a+')
        if level == "debug":
            logging.debug(message)
        elif level == "info":
            logging.info(message)
        elif level == "warning":
            logging.warning(message)
        elif level == "error":
            logging.error(message)
        elif level == "critical":
            logging.critical(message)
