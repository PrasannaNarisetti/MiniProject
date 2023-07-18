from flask import Flask, render_template, request, send_from_directory
import ipaddress as ip
import pandas as pd
from urllib.parse import urlparse
import tldextract
import pickle
app = Flask(__name__)
@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

@app.route("/")
def home():
    return render_template("index.html")
def numdots(url):
    return url.count('.')
def numdelim(url):
    n = 0
    delimiters=[';','_','?','=','&']
    for each in url:
        if each in delimiters:
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
@app.route('/model', methods=['GET', 'POST'])
def model():
    url = request.form['search']
    black_list = pd.read_csv("/Users/PycharmProjects/minipro/black_list.csv")
    x = url in black_list
    if x:
        res = "URL seems to be not safe"
    else:
        features = pd.DataFrame(columns=["url","no of dots","no of delimiters","presence of hyphen","len of url","presence of at","presence of double slash","no of subdir","no of subdomain","len of domain","no of queries","is IP","type"])
        results = getFeatures(url, '1')
        classification_model = pickle.load(open('classification.pkl', 'rb'))
        features.loc[0] = results
        features = features.drop(['url', 'type'], axis=1).values
        prediction = classification_model.predict(features)
        if (prediction == 1):
            res = "URL seems to be safe"
        else:
            res = "URL seems to be not safe"
            new_df = [url]
            black_list.loc[len(black_list)] = new_df
            black_list.to_csv("/Users/PycharmProjects/minipro/black_list.csv", index=False)
    return render_template("index.html", Result=res)
if __name__ == "__main__":
    app.run(debug=True)