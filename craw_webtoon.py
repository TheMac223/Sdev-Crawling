from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, random, pyperclip, requests
import openpyxl

book = openpyxl.Workbook()
browser = webdriver.Chrome()

browser.implicitly_wait(random.randint(3, 5))
time.sleep(random.randint(3, 5))
# week = browser.find_element(By.CSS_SELECTOR, "#container > div.component_wrap.type2 > div.WeekdayMainView__daily_all_wrap--UvRFc")

def login() :
    browser.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")
    browser.implicitly_wait(random.randint(3, 5))
    time.sleep(random.randint(3, 5))

    id_element = browser.find_element(By.ID, "id")
    pyperclip.copy("cat5235")
    id_element.send_keys(Keys.CONTROL, "v")
    time.sleep(5)
    pw_element = browser.find_element(By.ID, "pw")
    pyperclip.copy("wnsgud321")
    pw_element.send_keys(Keys.CONTROL, "v")
    time.sleep(5)
    #browser.execute_script('document.getElementById("log.login").click();')
    login_button = browser.find_element(By.XPATH, '//*[@id="log.login"]')
    login_button.click()

def get_webtoon(num):
    browser.get("https://comic.naver.com/webtoon")
    day = browser.find_element(By.XPATH, f"//*[@id=\"container\"]/div[3]/div[2]/div[{num}]")
    day_text = day.find_element(By.TAG_NAME,"h3").text
    book.active.append(day_text.split('   '))
    print(day_text)
    i = 1
    next = 0
    while True:
        try:
            browser.get("https://comic.naver.com/webtoon")
            browser.implicitly_wait(random.randint(3, 5))
            time.sleep(random.randint(3, 5))
            href = browser.find_element(By.XPATH,f"//*[@id=\"container\"]/div[3]/div[2]/div[{num}]/ul/li[{i}]/a").get_attribute('href')
            title = browser.find_element(By.XPATH,f"//*[@id=\"container\"]/div[3]/div[2]/div[{num}]/ul/li[{i}]/div/a/span").text
            print(title)
            book.active.append(title.split('   '))
            page = 1
            sum = 0
            while True:
                if next == 1:
                    next = 0
                    break
                ep = 1
                browser.get(f"{href}&page={page}&sort=ASC")
                browser.implicitly_wait(random.randint(1, 3))
                time.sleep(random.randint(1, 3))
                str = browser.find_element(By.XPATH,"//*[@id=\"content\"]/div[3]/div[1]/div[1]").text
                end = int(str[2:str.find('화')])
                print(end)
                while True:
                    try:
                        episode = browser.find_element(By.XPATH,f"//*[@id=\"content\"]/div[3]/ul/li[{ep}]/a/div[2]/p/span").text
                        book.active.append(episode.split('   '))
                        print(episode)
                        ep+=1
                        sum+=1
                        print(sum)
                        if sum == end:
                            next = 1
                            break
                    except:
                        break
                time.sleep(2)   
                page+=1
            i+=1
        except:
            break

login()

for i in range(1,8):
    get_webtoon(i)
book.save("webtoon.xlsx")
book.close()