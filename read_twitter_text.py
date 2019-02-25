import requests
from bs4 import BeautifulSoup
import pickle
import csv
from selenium import webdriver

twitter_data = {}

def get_tweets():
    browser = webdriver.Chrome()
    f_path = "/Volumes/sanket_drive/WebCrawledData/"
    f_name_path1 = f_path + "ws_crawled_more_features.csv"


    twitter_data_link = {"ws_name": [], "social": []}

    with open(f_name_path1, encoding="ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        line_count = 0
        _link_count = 0
        twitter_links = {}

        try:
            for row in csv_reader:
                tweet_str = ""
                if line_count > 0:
                    if "http" in row[8] and "twitter" in row[8]:
                        if row[8] not in twitter_links:
                            tweet_str = goto_page_and_read(row[8], browser)
                            twitter_links[row[8]] = tweet_str
                        else:
                            tweet_str = twitter_links[row[8]]
                        _link_count += 1
                        print(_link_count)
                    elif "http" in row[7] and "twitter" in row[7]:
                        if row[7] not in twitter_links:
                            tweet_str = goto_page_and_read(row[7], browser)
                            twitter_links[row[7]] = tweet_str
                        else:
                            tweet_str = twitter_links[row[7]]
                        _link_count += 1
                        print(_link_count)


                twitter_data[row[0]] = [row[8], tweet_str]

                line_count += 1



            print(_link_count)
            saving_tweets()


        except Exception as e:
            print(e)
            print(row)
            print("Error occuureed!!")
            saving_tweets()

def goto_page_and_read(t_link, browser):
    tweets_str = ""
    r = None
    try:

        r = requests.get(t_link, allow_redirects=False)
        if r.status_code!=200:
            return ""
    except (
    requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, requests.exceptions.RequestException) as e:
        print("Error occurred in requests!!")
        print(e)
        saving_tweets()

    if r is not None:
        try:
            browser.get(t_link)  # navigate to the page
            innerHTML = browser.execute_script("return document.body.innerHTML")
            soup = BeautifulSoup(innerHTML)
        except Exception:
            print("Error occurred in BeautifulSoup!!")
            print(e)
            saving_tweets()

        tweets_p = soup.find_all("p")


        link = ""
        if tweets_p is not None:
            for row in tweets_p:
                #tweet = row.select(".tweet-text")
                tag_attributes = row.attrs
                if 'class' in tag_attributes:
                    if "tweet-text" in row['class']:
                        tweets_str+= " "+row.text
    else:
        return ""

    return tweets_str

def saving_tweets():
    print("Storing got called")
    tweets = None


    '''with open('ws_tweets.pickle', 'rb') as handle:
        tweets = pickle.load(handle)'''

    if tweets is not None and len(tweets) > 0:
        print("Greater than zero!!")
        for key, val in twitter_data.items():
            tweets[key] = val

        with open('ws_tweets.pickle', 'wb') as handle:
            pickle.dump(tweets, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        with open('ws_tweets.pickle', 'wb') as handle:
            pickle.dump(twitter_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    for k, v in twitter_data.items():
        print(k + ": " + v[1])
        print("*************************************************")

def check_tweets():
    tweets =None
    with open('ws_tweets.pickle', 'rb') as handle:
        tweets = pickle.load(handle)
    count  = 0
    '''with open('ws_tweets.csv', mode='w', newline='') as csvfile:
        fieldnames = ['ws_name', 'tweets']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for k, v in tweets.items():
            writer.writerow({fieldnames[0]: k, fieldnames[1]: v})
            if len(v)>10:
                print(k+": "+v)
                print("*************************************************")
                count+=1
    print(count)'''

    for k, v in tweets.items():
        if len(v[1])>200:
            count+=1
            print(k+": "+v[1])

    print(count)

def get_ws_with_Same_tweets():
    tweets = None
    list_of_ws_having_same_tweeter={}
    with open('ws_tweets_copy.pickle', 'rb') as handle:
        tweets = pickle.load(handle)
        for k,v in tweets.items():
            if len(v)>100:
                if v not in list_of_ws_having_same_tweeter:
                    list_of_ws_having_same_tweeter[v] = [k]
                else:
                    list_of_ws_having_same_tweeter[v].append(k)

    with open('list_of_ws_having_same_tweeter_hndl.pickle', 'wb') as handle:
        pickle.dump(list_of_ws_having_same_tweeter, handle, protocol=pickle.HIGHEST_PROTOCOL)

    for k, v in list_of_ws_having_same_tweeter.items():
        print(v)
    print(len(list_of_ws_having_same_tweeter))

def concatenating_tweets_to_ws_desc():
    f_path = "/Volumes/sanket_drive/WebCrawledData/"
    csv_file_path = f_path + "ws_crawled_data.csv"

    full_ws_data = {}
    count=0
    tweets = None
    with open('ws_tweets.pickle', 'rb') as handle:
        tweets = pickle.load(handle)

    with open(csv_file_path, encoding="ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')


        for row in csv_reader:
            if count>0 and row[0] in tweets:
                desc = row[1]+" "+tweets[row[0]][1]
                full_ws_data[row[0]] = {"desc":desc, "primary":row[3], "secondary":row[4]}
            count+=1


    with open('full_ws_data.pickle', 'wb') as handle:
        pickle.dump(full_ws_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    test = None
    with open('full_ws_data.pickle', 'rb') as handle:
        test = pickle.load(handle)


    for k, v in test.items():
        print(v)
    print(len(test))









if __name__ == '__main__':
    concatenating_tweets_to_ws_desc()
