import io
import json
import os

# For Model 1 - HAND
from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request
import torch
from Preprocess import Preprocess
from models import HierAttNet, SentAttNet, WordAttNet

# 뉴스기사 크롤링
import requests
from bs4 import BeautifulSoup
import re
from flask import Flask, request, jsonify
from urllib.parse import unquote

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# For Model 1 - HAND
dict_path = os.path.join(APP_ROOT, 'ko_w2v_version2.txt')
model = HierAttNet(64,64,32,2,dict_path,20,32)
checkpoint_path = os.path.join(APP_ROOT, 'Model_Saved_dict.pth')
checkpoint = torch.load(checkpoint_path)
model.load_state_dict(checkpoint['model_state_dict'])
#model = torch.load(checkpoint_path, map_location=torch.device('cpu'))

    
def get_prediction(input_text):
    input_array = Preprocess(input_text)
    feature = torch.from_numpy(input_array)
    with torch.no_grad():
        model._init_hidden_state(2)
        prediction = model(feature)
    prediction = torch.nn.functional.softmax(prediction, dim=-1)
    max_prob, max_prob_index = torch.max(prediction, dim=-1)
    prob = "{:.2f}".format(float(max_prob[0])*100)

    clickbaitClass = True if max_prob_index[0] == 0 else False
    
    if clickbaitClass == False:
       return clickbaitClass, prob
    
    else:
        clickbaitClass == True
        clickbaitClass = False
        max_prob[0] = 1.0 - max_prob[0]  # 1에서 뺀 값으로 변경
        prob = "{:.2f}".format(float(max_prob[0]) * 100)
    return clickbaitClass, prob
    

# 뉴스 기사 링크를 받아서 입력데이터 형태로 반환
def get_news_from_link(news_url):
    ## 입력 예시: ######### 'https://entertain.naver.com//read?oid=112&aid=0003649533&cid=1073788'
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}
    # 여기 혹시 돌리는 사람에 따라서 헤더 수정해야 할 수도 있음
    resp = requests.get(news_url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # 뉴스기사 제목 찾기 (+전처리)
    title_element = soup.find(id='browse_title')
    news_title = title_element.text.replace(" :: 네이버 TV연예", "")
    news_title = re.sub(r'\s*[\(\[]\s*[^\)\]]+\s*[\)\]]\s*', '', news_title)
    # 뉴스기사 본문 찾기
    em_elements = soup.find(id='articeBody')
    news_contents = em_elements.text.replace('\n','')
    news = news_title + ". "+news_contents
    return news, news_title


def for_debugging(news_title, clickbaitClass, prob):
    print(f"News Title: {news_title}")
    print(f"clickbait: {clickbaitClass}, probability: {prob}")
    print("\n")



@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        link = request.args.get('link')  # 'link' 쿼리 매개변수 값을 가져옴
        if link:
            # URL 디코딩하여 링크 값을 제대로 받아옴
            decoded_link = unquote(link)
            # return f"Received link: {decoded_link}"
            
            news, news_title = get_news_from_link(decoded_link)
            clickbaitClass, prob = get_prediction(news)
    # 확인용으로 터미널에 뉴스 제목과 결과 출력하는 함수 => 영상 녹화할때 보이게 하면 좋을듯!
            for_debugging(news_title, clickbaitClass, prob)

            return jsonify({'clickbaitClass': clickbaitClass, 'prob': prob})
           
        else:
            return "No link provided in the query parameter."
