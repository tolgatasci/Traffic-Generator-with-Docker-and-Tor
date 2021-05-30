#!/usr/bin/python3
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import re
from collections import Counter
from urllib.parse import urlparse
from fake_useragent import UserAgent
import argparse
WEBURL = "https://www.eniyiuygulama.com/"
PROXY = "socks5://127.0.0.1:9050"
LIMIT = 5
VISIT = 0
RUN = True
WAIT = 10
FOLLOW_URL = True
HISTORY = [WEBURL]
DEBUG = True
PARSE_URL = urlparse(WEBURL)
driver = None
def referance():
    if len(HISTORY) > 1:
        driver.execute_script('window.location.href = "{}";'.format(HISTORY[-1]))
        if DEBUG:
            print("History setup %s" % HISTORY[-1])
def setup():
    global driver
    ua = UserAgent()
    user_agent = ua['google chrome']

    chrome_options = webdriver.ChromeOptions()
    # specify headless mode
    chrome_options.add_argument('headless')
    chrome_options.add_argument("--window-size=1920,1080")

    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    driver = webdriver.Chrome(executable_path="/chromedriver/chromedriver",options=chrome_options)
    driver.get(WEBURL)
    if FOLLOW_URL:
        search_url(driver)
def start():
    global VISIT, WEBURL, FOLLOW_URL

    referance()
    if FOLLOW_URL:
        search_url(driver)
    VISIT += 1
    if DEBUG:
        if driver.get_log("browser"):
            print(driver.get_log("browser"))
    time.sleep(WAIT)



def search_url(driver):
    global HISTORY, WEBURL
    elements = driver.find_elements_by_xpath("//a[@href]")
    all_links = []
    for element in elements:
        key = "#"
        url_new = re.sub(key+'.*', key, element.get_attribute("href"))
        all_links.append(url_new.replace("#",""))
    best_links = Counter(all_links)

    for url, count in sorted(best_links.items(), key=lambda x: x[1], reverse=True):
        url_parse = urlparse(url)
        if url not in HISTORY and url_parse.netloc.find(PARSE_URL.netloc) > -1:
            HISTORY.append(url)
            WEBURL = url
            break
    if DEBUG:
        print("next URL %s" % WEBURL)
def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False
if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-u", "--url",  default="https://www.eniyiuygulama.com/")
    parser.add_argument("-w", "--wait",  default=1)
    parser.add_argument("-l", "--limit",  default=0)
    parser.add_argument("-d", "--debug",  default=False)
    parser.add_argument("-loop", "--loop", default=1)
    args = parser.parse_args()
    if args.wait is not None:
        WAIT = int(args.wait)
    if args.limit is not None:
        LIMIT = int(args.limit)
    if args.debug is not None:
        DEBUG = bool(args.debug)
    if is_url(args.url):
        WEBURL = args.url
        print(args.url)
    setup()
    while RUN:
        start()
        if VISIT > LIMIT:
            RUN = False
            driver.close()
