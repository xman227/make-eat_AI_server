import torch
from PIL import Image
import json
from flask import Flask, jsonify, request, make_response
import os

file_path = "./Makeat_foodlist.json"
with open(file_path, encoding='utf-8') as f:
    foodlist = json.load(f)

app = Flask(__name__)


# 선택지 1 base64 로 보내기
# 선택지 2 Uint8List 로 보내기
# 선택지 3 list 로 보내기
# 선택지 4 안보내기

@app.route("/image", methods=['POST'])
def test():
    if request.method == 'POST':
        print('POST')

        file = request.files['image']

        print(f'사진의 이름과 형태는 : {file}')

        device = torch.device('cpu')
        # 업로드한 pt model 주소
        model = torch.hub.load('ultralytics/yolov5', 'custom', './best.pt',force_reload=False)  
        model.to(device)

        # 결과 반환
        img = Image.open(file)
        results = model(img)
        detection_index_list = list(results.pandas().xyxy[0]['class'])

        # 결과 사진 저장
        #save_dir = './result'   #원하는 경로로 변경가능
        #results.save(save_dir=save_dir, exist_ok=True)     
        
        #최종적으로 가는 내용물
        detection_dic = {"foodCount":0, "foodList":[]}
        
        for i in detection_index_list:
            detection_dic["foodCount"] += 1
            detection_dic["foodList"].append(foodlist[i])

        
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