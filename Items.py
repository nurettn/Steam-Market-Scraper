from bs4 import BeautifulSoup as soup
from fake_useragent import UserAgent
from selenium import webdriver
import time
import csv
from Common import Common

delay_time = 10
m_cMaxPages = 5


def run():
    driver = Common.getDriver()
    items_link = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_Pistol&category_730_Type%5B%5D=tag_CSGO_Type_SMG&category_730_Type%5B%5D=tag_CSGO_Type_Rifle&category_730_Type%5B%5D=tag_CSGO_Type_SniperRifle&category_730_Type%5B%5D=tag_CSGO_Type_Shotgun&category_730_Type%5B%5D=tag_CSGO_Type_Machinegun&appid=730#p1_popular_desc'
    driver.get(items_link)
    Common.collapsePage(driver, 100)
    # m_cMaxPages = Common.getcMaxPages(driver)
    for pageCount in range(1, m_cMaxPages):
        time.sleep(delay_time)
        Common.sendLog("info", 'There {0}. Items page analyzing'.format(Common.getiCurrentPage(driver)))
        containers = Common.getContainers(driver)
        for container in containers:
            item_name = Common.getItemName(container)
            item_normalPrice = Common.getNormalPrice(container)
            item_salePrice = Common.getSalePrice(container)
            item_count = Common.getItemCount(container)
            item_link = Common.getItemLink(container)
            Common.printToFile("Items.csv", item_name, item_normalPrice, item_salePrice, item_count, item_link)
        Common.NextPage(driver)
