import requests
from bs4 import BeautifulSoup
import pickle
import csv
from selenium import webdriver

def get_tweets():
    f_path = "/Volumes/sanket_drive/WebCrawledData/"
    f_name_path1 = f_path + "ws_crawled_more_features.csv"
    f_name_path2 = f_path + "ws_crawled_data.csv"

    twitter_data_link = {"ws_name": [], "social": []}
    twitter_data = {"ws_name": None}

    with open(f_name_path1, encoding="ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        line_count = 0
        _link_count = 0
        tweet_l = []
        try:
            for row in csv_reader:
                if line_count > 0:
                    if "http" in row[8] and "twitter" in row[8]:
                        tweet_l = goto_page_and_read(row[8])

                line_count += 1

            twitter_data["ws_name"] = tweet_l
            print(_link_count)


        except Exception as e:
            print(e)
            print(row)
            print("Error occuureed!!")

def goto_page_and_read(t_link):
    browser = webdriver.Chrome()  # replace with .Firefox(), or with the browser of your choice
    url = "http://example.com/login.php"
    browser.get(url)  # navigate to the page
    tweets_list = []
    r = None
    try:
        r = requests.get(t_link, allow_redirects=False)
        if r.status_code!=200:
            return []
    except (
    requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, requests.exceptions.RequestException) as e:
        print("Error occurred in requests!!")
        print(e)

    if r is not None:
        try:
            soup = BeautifulSoup(r.text)
        except Exception:

            print("Error occurred in BeautifulSoup!!")
            print(e)

        tweets_p = soup.body
        b = tweets_p.p


        link = ""
        if tweets_p is not None:
            for row in b:
                tweets_list.append(row)
    else:
        return []

    return tweets_list

if __name__ == '__main__':
    get_tweets()
