import requests
import json



url = 'http://localhost:3000/predict'
input = "https://entertain.naver.com//read?oid=112&aid=0003649533&cid=1073788"



resp = requests.post(url, data={"text": input})
                     
print(resp)
print(resp.json())


