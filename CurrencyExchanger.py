import requests
import json
import locale
from Common import Common

#currencyJSON = response.json() # Euro based currency
# coefficient = currencyJSON["rates"]['EUR']
class CurrencyExchanger(object):
    @staticmethod
    def updateCurrencyJSONFile():
        api_key = "API_KEY" #fixer.io/dashboard
        url = "http://data.fixer.io/api/latest?access_key=" + api_key
        response = requests.get(url)
        currencyJSON = response.json() # Euro based currency
        with open('currency.json', 'w') as f:
            json.dump(currencyJSON, f,indent=4)
    

currencyJSON = json.load(open("currency.json"))
steam_currencies =      ['A$', 'ARS$',   None,  'R$', 'CDN$',  'CHF',  'CLP$',    None,  'COL$',   '₡',   '€',   '£', 'HK$',   '₪',  'Rp',   '₹',   '¥',   '₩',  'KD',    '₸', 'Mex$',  'RM',  'kr', 'NZ$',  'S/.',    'P',   'zł',   'QR',  'pуб',   'SR',   'S$',   '฿',  'TL',  'NT$',   '₴',   '$',  '$U',  '₫',     'R', 'kr']
ISO4217_CurrencyCodes = ['AUD','ARS' ,  'AUD', 'BRL',  'CAD',  'CHF',   'CLP',  'CNY',  'COP',  'CRC', 'EUR', 'GBP', 'HKD', 'ILS', 'IDR', 'INR', 'JPY', 'KRW', 'KWD',  'KZT',  'MXN', 'MYR', 'NOK', 'NZD',  'PEN',  'PHP',  'PLN',  'QAR',  'RUB',  'SAR',  'SGD', 'THB', 'TRY',  'TWD', 'UAH', 'USD', 'UYU', 'VND',  'ZAR','SEK']


def convertPrice(gelenDeger='$9999999,999999 USD', istenen_currency='TRY') -> str:
    """
    Price converter MAIN function.
    Gelen ham string değerini alır, currency ve price bilgilerini çeker.
    Fiyatı istenen para birimine çevirir ve string şeklinde döndürür
    Return örneği = 35.894 TRY
    Örnek kullanım: newVal = convertPrice('1,58€', 'USD')
    Not: '--€' Euro döndürür
    """
    istenen_currency = istenen_currency.upper() # karakterleri uppercase yap
    #gelenDeger = '2390,35 pуб.'
    gelenDeger = makeReadable(gelenDeger)
    foreign_currency = getISOCurrencyFromString(gelenDeger) 
    actualPriceWithForeignCurrency = getPriceFromString(gelenDeger) # base fiyatı al
    finalPrice = getEquivalentValue(actualPriceWithForeignCurrency, foreign_currency, istenen_currency) # fiyatı çevir
    finalPrice = locale.format("%.2f", finalPrice, grouping=True) # virgülden sonrasını 2 basamak olarak ayarla
    #finalPrice = str(finalPrice) + " " + istenen_currency # fiyat + hedef para birimi şeklinde string oluştur
    return finalPrice
def getISOCurrencyFromString(s) -> str:
    """ 
    Steam'den gelen para biriminin ISO kodunu getirir.
    """
    steamCurrency = getCurrencySymbolFromString(s)

    # '$2.05 USD' -> '$.  USD' -> '$'
    if '$' in steamCurrency and 'USD' in steamCurrency:
        steamCurrency = '$'


    iso_equivalent_currency = ISO4217_CurrencyCodes[steam_currencies.index(steamCurrency)]
    return iso_equivalent_currency

def makeReadable(s) -> str:
    """ Virgülü noktayla değiştirir ve tireleri siler, sağdan soldan noktaları siler """
    s = s.replace(',','.')
    s = s.replace('-','')
    s = s.strip('.')
    return s
    
def getPriceFromString(s) -> float:
    """
    İlk virgülü noktayla değiştirir
    Firstly replaces colon with dot, deletes digits and strips with space, dot, colon and dash characters.
    """
    #number = ''.join((character if character in '0123456789.e' else '') for character in s)
    number = ''.join((character if character in '0123456789.' else '') for character in s)

    try:
        if len(number)>7:
            number = number.replace('.', '',1)
            number = float(number)
        else:
            number = float(number)
    except Exception as e:
        Common.sendLog("critical",e)
        
    
    return number

def getCurrencySymbolFromString(s) -> str:
    """
    Firstly deletes digits and strips with space, dot, colon and dash characters.
    """
    symbol = ''.join([i for i in s if not i.isdigit()])
    symbol = symbol.strip(".,- ")
    return symbol

def getEquivalentValue(price, steamCurrency, targetCurrency='TRY') -> float:
    
    # Eger iki currency türü aynıysa fiyatı aynen döndür
    if steamCurrency == targetCurrency:
        return price

    convertedPrice = 0.0
    baseKatsayi = 0.0
    hedefKatsayi = 0.0
        
    # foreignCurrency'nin Euro(base) oldugu durumda base kontrolü
    if steamCurrency == 'EUR':
        baseKatsayi = 1.0
    else:
        baseKatsayi = float(currencyJSON["rates"][steamCurrency])

    # base ve hedef katsayilari çek
    hedefKatsayi = float(currencyJSON["rates"][targetCurrency])
    convertedPrice = price * hedefKatsayi / baseKatsayi
    return convertedPrice

def testValues(*args) -> None:
    """
    Fonksiyonları test eder. 
    Test edilecek yeni değerleri metoda liste şeklinde 
    verilebilir veya aşağıdaki değişkene eklenebilir
    """
    testList = [
        '$1,095.85 USD',
        '¥ 16.50',
        '833,03 pуб',
        '$11.99 USD',
        '2390,35 pуб.',
        'R$ 13,05',
        '220,--€',
        '1,58€',
        'A$ 50.00',
        '₪57.00',
        'HK$ 300.00',
        'CDN$ 2.77',
        '£12.25',
        'RM69.58',
        'Mex$ 52.99'
        ]
    if len(args) > 0:
        for newValues in args:
            testList.append(newValues)
    print('-'*30)
    print("Değerleri yine de gözle test ediniz...")
    for val in testList:
        try:
            print("Input: " + val + '\t\t'+ '-----> ' + convertPrice(val, 'TRY') + '  --> ' + ' \t\tBAŞARILI')
        except Exception:
            print("<-----HATA!----HATA!-----HATA!-----> ŞU DEĞERDE HATA VAR:" , val)
            continue
    print("Test bitmiştir...")
    print('-'*30)


