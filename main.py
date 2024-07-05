import cloudscraper
import requests

#url = 'https://p2pbroker.xyz/login';
url = 'https://arh.antoinevastel.com/bots/areyouheadless'
session = requests.session()

def main(url, sess):
    scraper = cloudscraper.create_scraper(disableCloudflareV1=True, browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False
    }, debug=True, delay=50, sess=session)
    print(scraper.get(url))


if __name__ == '__main__':
    main(url, session)
