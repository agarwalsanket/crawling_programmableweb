import pickle
def dummy():
    with open('ws_links.pickle', 'rb') as handle:
        res1 = pickle.load(handle)
        print(len(res1))

if __name__ == '__main__':
    dummy()
