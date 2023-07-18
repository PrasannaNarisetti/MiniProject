import time
import ipaddress as ip
import pandas as pd
import tldextract
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
def numdots(url):
    return url.count('.')
def numdelim(url):
    n = 0
    delim=[';','_','?','=','&']
    for each in url:
        if each in delim:
            n = n + 1
    return n
def ipornot(url):
    try:
        if ip.ip_address(url):
            return 1
    except:
        return 0
def forhyphen(url):
    return url.count('-')
def forat(url):
    return url.count('@')
def fordoubleslash(url):
    return url.count('//')
def forsub(url):
    return url.count('/')
def countsub(subdomain):
    if not subdomain:
        return 0
    else:
        return len(subdomain.split('.'))
def forquery(query):
    if not query:
        return 0
    else:
        return len(query.split('&'))
from urllib.parse import urlparse
def getFeatures(url, label):
    feature_extraction = []
    url = str(url)
    feature_extraction.append(url)
    path = urlparse(url)
    ext = tldextract.extract(url)
    feature_extraction.append(numdots(ext.subdomain))
    feature_extraction.append(numdelim(ext.subdomain))
    feature_extraction.append(forhyphen(path.netloc))
    feature_extraction.append(len(url))
    feature_extraction.append(forat(path.netloc))
    feature_extraction.append(fordoubleslash(path.path))
    feature_extraction.append(forsub(path.path))
    feature_extraction.append(countsub(ext.subdomain))
    feature_extraction.append(len(path.netloc))
    feature_extraction.append(len(path.query))
    feature_extraction.append(ipornot(ext.domain))
    feature_extraction.append(str(label))
    return feature_extraction

start_time = time.time()

blacklist = pd.read_csv("/Users/PycharmProjects/miniproject/black_list.csv")
data_for_modal = pd.read_csv("urls.csv")
x = data_for_modal.drop(['url', 'type'], axis=1).values
y = data_for_modal['type'].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=500)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)

random_forest_total_time = 0
blacklist_total_time = 0
using_both_time =0

def timecamp(url):
    start_time = time.time()
    features = pd.DataFrame(
        columns=["url", "no of dots", "no of delimiters", "presence of hyphen", "len of url", "presence of at",
                 "presence of double slash", "no of subdir", "no of subdomain", "len of domain", "no of queries",
                 "is IP", "type"])
    results = getFeatures(url, '1')
    features.loc[0] = results
    features = features.drop(['url', 'type'], axis=1).values
    model.predict(features)
    random_forest_total_time= time.time() - start_time
    # Blacklist Lookup
    start_time = time.time()
    is_blacklisted = url in blacklist
    blacklist_total_time = time.time() - start_time
    start_time = time.time()
    x = url in blacklist
    if x:
        x
    else:
        features = pd.DataFrame(
            columns=["url", "no of dots", "no of delimiters", "presence of hyphen", "len of url", "presence of at",
                     "presence of double slash", "no of subdir", "no of subdomain", "len of domain", "no of queries",
                     "is IP", "type"])

        results = getFeatures(url, '1')
        features.loc[0] = results
        features = features.drop(['url', 'type'], axis=1).values
        model.predict(features)
    using_both_time = time.time() - start_time
    print(f'Random Forest Average Classification Time: {random_forest_total_time } seconds')
    print(f'Blacklist Average Lookup Time: {blacklist_total_time} seconds')
    print(f'Using both Lookup Time: {using_both_time} seconds')
url=str(input("enter:"))
timecamp(url)
