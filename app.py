import torch
from PIL import Image
import json
from flask import Flask, jsonify, request, make_response

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
        data = request.get_json()
        #client에서 post하려고 요청 온 데이터를 해당 방식으로 추출
        #post 방식의 경우에는 데이터뿐 아니라 다양한 값들이 필요한 데이터와 섞여서 오기 때문에 
        #우선 데이터 추출하는 과정이 필요
        #print(data)
        # 그러면 데이터가 딕셔너리형태로 추출
        #print(data['url'])
        # 그러면 서버에서 데이터 처리에 필요한 데이터 기준으로 키값으로 데이터 "저장"

        image_path = data['url']  #앱에서 촬영된 사진경로


        device = torch.device('cpu')
        model = torch.hub.load('ultralytics/yolov5', 'custom', './best.pt',force_reload=False)  
        # 업로드한 pt model 주소
        
        model.to(device)

        #save_dir = './result'   #원하는 경로로 변경가능

        # Load the image using PIL
        img = Image.open(image_path)

        # Run detection on the image
        results = model(img)
        
        #results.save(save_dir=save_dir, exist_ok=True)     
        #디텍팅된 사진 저장
        
        detection_index_list = list(results.pandas().xyxy[0]['class'])

        detection_name_list = []
        detection_dic = {}
        
        if detection_index_list == []:
            return make_response(jsonify({'foodlist': ['none'] }), 200)
        
        for i in detection_index_list:
            detection_name_list.append(foodlist[i])

        
        #results.render()

        detection_dic["foodlist"] = detection_name_list
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
    app.run(host='0.0.0.0')            
    #app.run(host='127.0.0.1', port=5000)