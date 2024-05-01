import requests
import json
import pandas as pd

# 요청 헤더 설정
headers = {
    'Host': 'cmapi.coupang.com',
    'Coupang-App': 'COUPANG|Android|9|8.1.4||cwWD2dt3R7Gr1JZJKAIlTp:APA91bEuA7iCLVp2r0HAfszc9qLgCZ2a-yNQpkGphcv6ivmWHHOeayi7gjKVqxVY6PSN5inENL10_CzIPiFBY8y4qqV7t7R9fNwH2qDCPd9RiO19a8slSNVS4t-Q1H3MfccKyzoQLsoi|394bb9f1-cca8-30ba-ae0d-16781c59bc71|Y|SM-G955N|394bb9f1cca870baae0d16781c59bc71|abbcc3ac-c640-4dfe-9392-ce7c80e2e68f|XHDPI|17145165212601283084445||0||wifi|-1|||Asia/Seoul|31ca2ea9e2114e3796b74185db819928f698c024||1600|320|4|1.0|true',
    'Run-Mode': 'production',
    'X-Cmg-Dco': '1714514135130',
    'X-Coupang-Origin-Region': 'KR',
    'X-Lightspeed-Access-Token': '',
    'X-Cp-App-Req-Time': '1714530988694',
    'X-View-Name': '/search',
    'X-Coupang-Target-Market': 'KR',
    'Accept-Language': 'ko-KR',
    'X-Coupang-Accept-Language': 'ko-KR',
    'X-Trace-Ix-Id': '00000364-5770-75de-e139-53a0ab7e4adb',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; SM-G955N Build/NRD90M.G955NKSU1AQDC)',
    'Accept-Encoding': 'gzip, deflate, br'
}

# 요청 보낼 URL
url = 'https://cmapi.coupang.com/v3/products?filter=KEYWORD:%EC%BC%80%EC%9D%B4%ED%81%AC|CCID:ALL|EXTRAS:channel/user|GET_FILTER:NONE|SINGLE_ENTITY:TRUE@SEARCH&preventingRedirection=false&enableQATC=false&resultType=default&ccidActivated=false'

# GET 요청 보내기
response = requests.get(url, headers=headers)

# 응답 확인
if response.status_code == 200:
    print("요청이 성공했습니다.")
else:
    print(f"요청 실패: {response.status_code}")

with open('coupang.json', 'w',encoding='utf-8') as json_file:
    json.dump(response.json(), json_file,ensure_ascii=False,      indent=4)

data = response.json()

lst = [{},]
i = 1


for _ in range(len(data["rData"]["entityList"])-1):
    try:
        print(i)
        lst.append({"title" : data["rData"]["entityList"][i]["entity"]["displayItem"]["title"],
                  "salesPrice" : data["rData"]["entityList"][i]["entity"]["displayItem"]["salesPrice"]})
        i += 1
    except KeyError:
        i += 1
        continue



df = pd.DataFrame(lst)

file_path = 'coupang.xlsx'  
df.to_excel(file_path, index=False) 

print(f'Excel 파일이 저장되었습니다: {file_path}')


