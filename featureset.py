import pandas as pd
import numpy as np
import ipaddress as ip
import tldextract
df = pd.read_csv("malicious_phish.csv")
df = df.sample(frac=1).reset_index(drop=True)
condition = df['type'] == 'benign'
df['label'] = np.where(condition, 1, 0)
df.drop('type', axis=1, inplace=True)
def numdots(url):
    return url.count('.')
def numdelim(url):
    count = 0
    delim=[';','_','?','=','&']
    for each in url:
        if each in delim:
            count = count + 1
    return count
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
featureSet = pd.DataFrame(columns=["url","no of dots","no of delimiters","presence of hyphen","len of url","presence of at","presence of double slash","no of subdir","no of subdomain","len of domain","no of queries","is IP","type"])
for i in range(len(df)):
    features = getFeatures(df["url"].loc[i], df["label"].loc[i])
    featureSet.loc[i] = features
filtered_df = featureSet[~(featureSet.astype(str).apply(lambda x: x.str.len() > 250).any(axis=1))]
filtered_df.to_csv("urls.csv", index=False)

