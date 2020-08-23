from bs4 import BeautifulSoup as soup
from fake_useragent import UserAgent
from selenium import webdriver
import time
import re
import json
from Common import Common

delay_time = 10


def run():
    driver = Common.getDriver()
    # sticker_link = "https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_StickerCategory%5B%5D=tag_PlayerSignature&category_730_StickerCategory%5B%5D=tag_TeamLogo&category_730_StickerCategory%5B%5D=tag_Tournament&appid=730"
    # sticker_link = "https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B0%5D=any&category_730_ProPlayer%5B0%5D=any&category_730_StickerCapsule%5B0%5D=any&category_730_TournamentTeam%5B0%5D=any&category_730_Weapon%5B0%5D=any&category_730_StickerCategory%5B0%5D=tag_PlayerSignature&appid=730"
    bicak_link = "https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_Knife&appid=730"
    # driver.get(sticker_link)
    driver.get(bicak_link)
    Common.collapsePage(driver, 100)
    m_cMaxPages = Common.getcMaxPages(driver)
    for pageCount in range(1, m_cMaxPages):
        time.sleep(delay_time)
        Common.sendLog("info", 'The {0}. sticker page is being analyzed'.format(Common.getiCurrentPage(driver)))
        containers = Common.getContainers(driver)
        for container in containers:
            item_name = Common.getItemName(container)
            item_normalPrice = Common.getNormalPrice(container)
            item_salePrice = Common.getSalePrice(container)
            item_count = Common.getItemCount(container)
            item_link = Common.getItemLink(container)
            # Common.printToFile("Sticker.csv",item_name, item_normalPrice, item_salePrice,item_count, item_link)
            Common.printToFile("Knife.csv", item_name, item_normalPrice, item_salePrice, item_count, item_link)
        Common.NextPage(driver)
    driver.quit()
