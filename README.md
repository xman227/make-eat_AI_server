# Food Detection AI using YOLOv5 🍽️
<br><br/>

## How to use
### 1. Install the dependencies
```sh
pip install -r requirements.txt
pip install ultralytics
```
IF you need `piltu`, you can install that using pip or pip3

### 2. Run the flask code
```sh
#Windows
flask run

#Mac
python3 app.py

```




### 3. request the post method.
you can post it to url of this : {your host}/image

```sh
{
    'url':'test_food.jpg'
}
```
<br><br/>



### 4. if you run code with production mode/
you can use AWS EC2 service.
```sh
#it depends on AMI - DL AMI GPU Pytorch 1.13.1 Linux2

sudo yum install git
git clone https://github.com/MAK-E-AT/AI.git
cd AI
pip install -r requirements.txt
pip install ultralytics
python3 app.py 



```

## Ref.

- AWS ec2 upload
https://itsjh.tistory.com/36
https://velog.io/@jaehyeong/Flask-%EC%9B%B9-%EC%84%9C%EB%B2%84-AWS-EC2%EC%97%90-%EB%B0%B0%ED%8F%AC%ED%95%98%EA%B8%B0

이 때 기존 프리티어 IMAGE 에는 torch 가 killed 돼서  
DL pytorch1.13.1 버전의 ec2 IMAGE 를 사용했다.
https://cinema4dr12.tistory.com/1314

- AWS ssh 접근 시 root 계정을 막을 때
https://asufi.tistory.com/entry/AWS-EC2-%EC%A0%91%EC%86%8D-root-%EA%B6%8C%ED%95%9C
