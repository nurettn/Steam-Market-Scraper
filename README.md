<h3 align = "center">
    <img src = "https://github.com/nurettinabaci/Steam-Market-Scraper/blob/master/Steam_Market_Scraper.png" alt = "Logo" />
</h3>

---
# Steam CS:GO Market Scraper
Very powerful Steam market scraper. Scans for items, for the lowest prices 
and scans item stickers. 
Prepares tailored message and sends it to Discord server via webhook.
Getting insight about Steam market items were never been so easy like that.
It is also possible to use this code in other game markets by making minor 
changes on it.


## Usage
   
   Firstly, install the project requirements after cloning the repo to your local. 
   
    pip install requirements.py
   
   Run whatever you need inside `main.py`, prepare your data and start to use them
   to get insight.
   Be careful about delays between requests, you can use proxies.

   
   You can compare the item prices with the other markets and buy & sell items.

   To convert prices fixer.io currency converter API is used. You can look at 
   the detailed information about converting currency from 
   [here](https://github.com/nurettinabaci/Steam-Currency-Converter).
   
   Also, you should provide webhook API link to send the messages to Discord server. 

## Contribution
Please open an issue if there is an unhandled currency value so we
can append it to codebase.

Pull requests are welcome. For major changes, please open an issue 
first to discuss what you would like to change.

## License
This repository is licensed under the MIT License. Please see the 
[LICENSE](https://github.com/nurettinabaci/Steam-Market-Scraper/blob/master/LICENSE)
file for more details.