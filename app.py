import torch
from PIL import Image
import json
from flask import Flask, jsonify, request, make_response
import os

file_path = "./Makeat_foodlist.json"
with open(file_path, encoding='utf-8') as f:
    foodlist = json.load(f)

app = Flask(__name__)

use_count = 0

@app.route("/image", methods=['POST'])
def test():
    if request.method == 'POST':

        if use_count == 0:
            device = torch.device('cpu')
            # 업로드한 pt model 주소
            model = torch.hub.load('ultralytics/yolov5', 'custom', './best.pt',force_reload=False)  
            model.to(device)
        
        use_count += 1

        # 결과 반환
        file = request.files['image'] #print(f'사진의 이름과 형태는 : {file}')
        results = model(Image.open(file))
    
        detection_index_list = list(results.pandas().xyxy[0]['class'])

        # 결과 사진 저장
        #save_dir = './result'   #원하는 경로로 변경가능
        #results.save(save_dir=save_dir, exist_ok=True)     
        
        #최종적으로 가는 내용물
        detection_dic = {"foodCount":0, "foodList":[], "foodName":[]}
        
        for i in detection_index_list:
            detection_dic["foodCount"] += 1
            detection_dic["foodList"].append(foodlist[i])
            detection_dic["foodName"].append(foodlist[i]["name"])

        
        #results.render()
        #detection_dic["image"] = results.render()[0].tolist()
        #print(f'이 이미지의 모양은 {results.render()[0].shape}')

        json_output = json.dumps(detection_dic, ensure_ascii=False, indent= 2)

        # with open('./json_output.json', 'w', encoding='utf-8') as outfile:
        #     json.dump(json_output, outfile, ensure_ascii=False, indent=2)
        return json_output
 
    return make_response(jsonify({'status': True}), 200)

@app.route('/')
def detection():

    return '1'


if __name__ == '__main__':
    #webbrowser.open()    #webbrowser.open('http://127.0.0.1:5000/')
    app.run(host='0.0.0.0', port=5000)            
    #app.run(host='127.0.0.1', port=5000)