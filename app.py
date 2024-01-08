import requests
import logging
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
from flask import Flask,render_template,request
logging.basicConfig(filename="scrapper.log",level=logging.INFO)


app = Flask(__name__)



@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
       try:
        save_dir = './images'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        query = request.form['query']
        response = requests.get(f"https://www.google.com/search?q={query}&sca_esv=596479318&rlz=1C1RXQR_enIN1089IN1089&tbm=isch&sxsrf=AM9HkKk350isCArIXJVhTUHj6clwk6dkGw:1704697917604&source=lnms&sa=X&ved=2ahUKEwit1M_Ons2DAxVGn2MGHbxRBzIQ_AUoAXoECAEQAw&biw=1920&bih=945&dpr=1")
        soup = BeautifulSoup(response.content,'html.parser')
        img_tag = soup.find_all('img')
        del img_tag[0]
        for x in img_tag:
            img_url = x['src']
            image_data = requests.get(img_url).content
            with open(os.path.join(save_dir,f"{query}_{img_tag.index(x)}.jpg"),"wb") as f:
                f.write(image_data)
        return render_template('success.html')
       except Exception as e:
           return e



if __name__ =='__main__':
    app.run()

