import requests
from bs4 import BeautifulSoup
import pickle
import csv

def get_mashup_all_link(ws_url):

    mashup_links = {}
    r = None
    try:
        r = requests.get(ws_url, allow_redirects=False)
    except (requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, requests.exceptions.RequestException) as e:
        store_in_pickle()
        print("Error occurred in requests!!")
        print(e)

    if r is not None:
        try:
            soup = BeautifulSoup(r.text)
        except Exception:
            store_in_pickle()
            print("Error occurred in BeautifulSoup!!")
            print(e)


        service_link_dr = soup.select('.view-all')
        link = ""
        for row in service_link_dr:
            if "Mashups" in row.text:
                link = "https://www.programmableweb.com/"+row["href"]
                mashup_links = get_all_mashups(link)
                break
        return mashup_links
    else:
        return {}


def get_all_mashups(all_mashup_link):
    link_storage = {}
    r = requests.get(all_mashup_link, allow_redirects=False)
    soup = BeautifulSoup(r.text)
    tbody_list = soup.find_all("tbody")
    data_in_this_page = []

    if len(tbody_list)>3:
        data_in_this_page = soup.find_all("tbody")[2].find_all("a")

    anchor_Selected = soup.select(".pager-next a")
    max_pgs = 0
    if anchor_Selected !=None and len(anchor_Selected)>=1:
        max_pgs = int(soup.select(".pager-next a")[0].text)


    while max_pgs>0:
        for row in data_in_this_page:
            if len(row.select("td")) == 0:
                if "https://www.programmableweb.com" not in row['href'] and 'category' not in row['href']:
                    link_storage[row.text] = "https://www.programmableweb.com/" + row['href']
                    print(row.text+": "+link_storage[row.text])
                else:
                    if 'category' not in row['href']:
                        link_storage[row.text] = row['href']

        if len(soup.select(".pager-last a")) > 0:
            curr_pg_url = "https://www.programmableweb.com/"+soup.select(".pager-last a")[0]['href']
            r_new = requests.get(curr_pg_url, allow_redirects=False)
            soup = BeautifulSoup(r_new.text)
            data_in_this_page = soup.find_all("tbody")[2].find_all("a")

        max_pgs-=1

    return link_storage

all_mashup_link_corr_ws = {}

def store_in_pickle():
    print("Storing got called")
    mashups_links = None
    with open('all_mashup_links_corr_ws.pickle', 'rb') as handle:
        mashups_links = pickle.load(handle)

    if mashups_links is not None and len(mashups_links)>0:
        print("Greater than zero!!")
        for key, val in all_mashup_link_corr_ws.items():
            mashups_links[key] = val

        with open('all_mashup_links_corr_ws.pickle', 'wb') as handle:
            pickle.dump(mashups_links, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        with open('all_mashup_links_corr_ws.pickle', 'wb') as handle:
            pickle.dump(all_mashup_link_corr_ws, handle, protocol=pickle.HIGHEST_PROTOCOL)

def get_all_mashup_description():
    mashups_links = None
    with open('all_mashup_links_corr_ws.pickle', 'rb') as handle:
        mashups_links = pickle.load(handle)
    without_mashups = 0
    with_mashups = 0


    for key, val in mashups_links.items():
        print(key)
        if len(val)==0:
            without_mashups+=1
            continue
        with_mashups+=1
        for k, v in val.items():
            print(k+": "+v)
        print("***************************************************************************")
        print("***************************************************************************")
        print("***************************************************************************")
    print("With mashups: " + str(with_mashups))
    print("Without mashups: "+str(without_mashups))

def print_ws_links():
    ws_links = None
    with open('ws_links.pickle', 'rb') as handle:
        ws_links = pickle.load(handle)

    for k, v in ws_links.items():
        print(k)
        print(v)
        print("***************************************************************************")














def main():
    '''global all_mashup_link_corr_ws
    with open('ws_links.pickle', 'rb') as handle:
        ws_links = pickle.load(handle)

    count = 0
    for key, val in ws_links.items():
        count += 1
        print(count)
        if count>4432:
            ws_name = key
            all_mashups_links_d = get_mashup_all_link(val)
            print(ws_name+", NO. of Mashups: "+str(len(all_mashups_links_d)))
            all_mashup_link_corr_ws[ws_name] = all_mashups_links_d



    store_in_pickle()
    print(count)
    count+=1

    print("succesfull completion")

    with open('all_mashup_links_corr_ws.pickle', 'rb') as handle:
        mashups_links = pickle.load(handle)
        count =0
        for key, val in mashups_links.items():
            print(key)
            if key=="Google Maps":
                for k,v in val.items():
                    print(k+": "+v)'''
    #get_all_mashup_description()
    #print_ws_links()




if __name__ == '__main__':
    main()

