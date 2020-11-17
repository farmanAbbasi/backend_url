from bs4 import BeautifulSoup
import requests
from flask import Flask
from flask import request
app = Flask(__name__)
import json
from flask_cors import CORS, cross_origin
CORS(app)

def getMovieUrl(movieName):
    url="http://putlockerstv.online/rogue-2020/"
    url = "http://123movies4u.site/"+movieName+"/"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    try:
        movieUrl=soup.find_all('iframe')[0]['src']
    except Exception as e:
        movieUrl=""
    return movieUrl


@app.route('/loadData', methods=['GET'])
def loadData():
    names=[]
    names.append(request.args.get('name1'))
    names.append(request.args.get('name2'))
    
    for name in names:
        finalName=getMovieUrl(name)
        #if got the url 
        if(finalName!=""):
            break
    return json.dumps({"url": finalName})    

@app.route('/', methods=['GET'])
def getData():
    return json.dumps({"msg": "hello"})
#http://127.0.0.1:5000/loadData?name1=ava-2020&name2=ava
if __name__ == '__main__':
    app.run()
    
        
