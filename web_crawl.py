import requests
from bs4 import BeautifulSoup
import pickle
import csv
'''
@Author: Sanket Agarwal
This code snippet crawls data from the website: https://www.programmableweb.com/.
It is a very specific web-crawling code, which can be used only for getting specific data.
'''

link_storage = {}



def get_links(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    service_link_dr = soup.find_all('tbody')[2].find_all("a")
    page = 0

    while page<730:
        for row in service_link_dr:
            if len(row.select("td")) == 0:
                if "https://www.programmableweb.com" not in row['href'] and 'category' not in row['href']:
                    link_storage[row.text] = "https://www.programmableweb.com/" + row['href']
                else:
                    if 'category' not in row['href']:
                        link_storage[row.text] = row['href']
                if row.text in link_storage:
                    print(row.text + ": "+link_storage[row.text])
                    print("-------------------------------------------")
        print("Priniting last")
        if len(soup.select(".pager-last a")) > 0:
            print(soup.select(".pager-last a")[0]['href'])
            curr_pg_url = "https://www.programmableweb.com/"+soup.select(".pager-last a")[0]['href']
            print(curr_pg_url)
            r = requests.get(curr_pg_url)
            soup = BeautifulSoup(r.text)
            service_link_dr = soup.find_all('tbody')[2].find_all("a")
        page += 1

    return link_storage

def read_data(ws_name, url):
    #print("inside add!")
    r = requests.get(url, allow_redirects=False)
    soup = BeautifulSoup(r.text)
    soup_desc = soup.select(".api_description")
    soup_categories = soup.select(".field")
    primary_category = None
    secondary_category = None

    for row in soup_categories:
        label = row.select("label")
        if len(label)>0 and label[0].text=="Primary Category":
            primary_category = row.select("a")[0].text if len(row.select("a"))>0 else None
            break
    for row in soup_categories:
        label = row.select("label")
        if len(label)>0 and label[0].text=="Secondary Categories":
            secondary_category = row.select("a")[0].text if len(row.select("a"))>0 else None
            break

    ws_description = soup_desc[0].text if len(soup_desc)>0 else None


    if ws_description is not None:
        print(ws_name)
        print(ws_description)
        print("___________________________________________________________")
        return [ws_name, ws_description, url,  primary_category, secondary_category]
    else:
        return []

def get_additional_info(ws_name, url):
    #print("inside add!")
    r = requests.get(url, allow_redirects=False)
    soup = BeautifulSoup(r.text)
    soup_categories = soup.select(".field")
    features_key = []
    features_key.append("ws_name")
    features_val = []
    features_val.append(ws_name)

    for row in soup_categories:
        label = row.select("label")
        if len(label)>0:
            features_key.append(label[0].text)
            if len(row.select("a"))>0:
                features_val.append(row.select("a")[0].text)
            elif len(row.select("span"))>0:
                features_val.append(row.select("span")[0].text)
            else:
                features_val.append(None)

    return features_key, features_val








def main():
    url = "https://www.programmableweb.com/category/all/apis"
    #res = get_links(url)
    res1 = None
    #with open('ws_links.pickle', 'wb') as handle:
        #pickle.dump(res, handle, protocol=pickle.HIGHEST_PROTOCOL)
    seen = set()

    with open('ws_links.pickle', 'rb') as handle:
        res1 = pickle.load(handle)


    count = 0
    i = 0
    features_name=[]
    features_value=[]



    print(count)

    res = []
    with open('ws_crawled_more_features.csv', 'a', newline='') as csvfile:
        count =0
        for key, val in res1.items():
            count += 1
            if count>=3747:
                features_name, features_value = get_additional_info(key, val)

                if len(features_value)>2:
                    print(features_name[0]+": "+features_name[2])
                    print(features_value[0]+": "+features_value[2])

                fieldnames = features_name
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if count <=1:
                    writer.writeheader()

                if len(features_name) and len(features_value)>0:
                    writer.writerow({fieldnames[i]: features_value[i] for i in range(len(features_name))})


    '''with open('ws_crawled_data1.csv', 'a', newline='') as csvfile:
        fieldnames = ['ws_name', 'description', 'URL','Primary Category', 'Secondary Category']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for key, val in res1.items():
            if val not in seen:
                seen.add(val)
                #print("calling add!")
                if i>count:
                    res = read_data(key, val)
                i+=1
            if len(res)>0:
                writer.writerow({fieldnames[0]: res[0], fieldnames[1]: res[1], fieldnames[2]: res[2],
                                 fieldnames[3]: res[3], fieldnames[4]: res[4]})'''

if __name__ == '__main__':
    main()



