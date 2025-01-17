import requests
from flask import Flask
from flask import request, jsonify
app = Flask(__name__)
import json
import os
from flask_cors import CORS, cross_origin
import openai

CORS(app)
openai.api_key = os.getenv("OPENAI_API_KEY")
wedding_info = """
You are a wedding assistant. The wedding details are as follows:
- The wedding or nikah date is 10th May 2025.
- The reception or walima is on 12th May 2025.
- The venue is at my village alawalpur, mau aima, allahabad.
- here is the location for google map https://www.google.com/maps/search/25.698925,+81.874286?entry=tts&g_ep=EgoyMDI1MDExMC4wIPu8ASoASAFQAw%3D%3D
- The wedding theme is a blend of traditional and modern decor with a color scheme of white and gold.
- The bride's name is Aqsa Moeez, and the groom's name is Mohammad Farman Ibrahim.
- Brides father is a lawyer and his name is Moeez uddin and her mother name is Parveen fatma
- Grooms father works in Hotel industry and his name is Islam uddin and her mother name is Parveen Bano
- Groom has 2 sisters , sadaf islam(B-pharma grad) and rifat islam (B-tech in AI/ML)
- Bride has 3 brothers , Zoheb, Muzammil and Mubassir in order of thier birth
- The guests are expected to arrive at 1 PM for the ceremony.
- The wedding includes no DJ.
- Grooms nani hosue is in Matyari and brides in Alawalpur itself
"""
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data['message']

        # Make the API call to OpenAI to get the assistant's reply
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Use GPT-4o-mini model
            messages=[
                {"role": "system", "content": wedding_info},
                {"role": "user", "content": user_message}
            ],
            timeout=20  # Adjust as needed

        )

        reply = response['choices'][0]['message']['content']

        return jsonify({'reply': reply})

    except Exception as e:
        # Extract meaningful error message
        error_message = str(e)
        if "Rate limit reached" in error_message:
            try:
                # Extract retry duration (if present)
                retry_time = error_message.split("Please try again in ")[1].split(" ")[0]
                meaningful_message = f"Please try again after {retry_time} seconds."
            except IndexError:
                meaningful_message = "Please try again later."
        else:
            meaningful_message = "An unexpected error occurred. Please try again later."

        # Log the error for debugging (optional)
        print(f"Error: {error_message}")

        # Send the meaningful error as the bot's response
        return jsonify({'reply': meaningful_message})


# def getMovieUrl(movieName):
#     url="http://putlockerstv.online/rogue-2020/"
#     url = "http://123movies4u.site/"+movieName+"/"
#     html_content = requests.get(url).text
#     soup = BeautifulSoup(html_content, "html.parser")
#     try:
#         movieUrl=soup.find_all('iframe')[0]['src']
#     except Exception as e:
#         movieUrl=""
#     return movieUrl

def getCorsEnabled(url,postData,requestMethod):
    if requestMethod == 'GET':
        return requests.get(url).json()
    else:
        #would pe post    
        return requests.post(url,json=postData).json()
   
     

@app.route('/enableCors', methods=['GET','POST'])
def cors():
    url=request.args.get('url')
    if request.method == 'GET':
        content=getCorsEnabled(url,{},request.method)
        return json.dumps(content)  
    else:
        fullData = request.json
        content=getCorsEnabled(url,fullData,request.method)
        return json.dumps(content)    
        

# @app.route('/loadData', methods=['GET'])
# def loadData():
#     names=[]
#     names.append(request.args.get('name1'))
#     names.append(request.args.get('name2'))
    
#     for name in names:
#         finalName=getMovieUrl(name)
#         #if got the url 
#         if(finalName!=""):
#             break
#     return json.dumps({"url": finalName})    

@app.route('/', methods=['GET'])
def getData():
    return json.dumps({"msg": "hello"})
#http://127.0.0.1:5000/loadData?name1=ava-2020&name2=ava
if __name__ == '__main__':
    app.run(debug=True,port=os.getenv("PORT",default=5000),host="0.0.0.0")
    
        
