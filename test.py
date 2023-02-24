import sys
import subprocess
import time
import re

def info_collect(driver):
    # 영상 정보 추출 (현재 날짜 밑 시간, 영상 이름, 채널명, 조회수, 게시일)
    import time
    from selenium.webdriver.common.by import By

    collection_date = time.strftime('%Y.%m.%d - %H.%M.%S')

    viedo_name = driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[1]/h1/yt-formatted-string').text

    channel_name = driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[1]/ytd-video-owner-renderer/div[1]/ytd-channel-name/div/div/yt-formatted-string/a').text

    views = driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[3]/div[1]/div/div/yt-formatted-string/span[1]').text.split(' ')[1]

    opening_date = driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[3]/div[1]/div/div/yt-formatted-string/span[3]').text

    result = {'수집 날짜':collection_date,'영상 이름':viedo_name,'채널 이름':channel_name,'조회수':views,'게시일':opening_date}

    return result
    

def scroll_down(driver):
    driver.set_window_size(800, 1100)
    
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
    time.sleep(1.5)

    #스크롤 이전 높이
    #화면 바깥으로 삐져나간 부분까지 포함해서 전체 글의 길이를 scrollHeight
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        #스크롤의 y좌표를 가장아래(scrollHeight)까지 내림
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1.5)

        #스크롤 후 높이 구하기
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        #끝까지 스크롤 한 뒤 멈추기
        if new_height == last_height:
            break
        last_height = new_height

        time.sleep(1.5)
    
    return 0

def open_reply(driver):
    from selenium.webdriver.common.by import By

    replies = driver.find_elements(By.CLASS_NAME,"more-button")

    driver.implicitly_wait(10)

    for reply in replies:
        driver.execute_script("arguments[0].click();", reply)
        time.sleep(1.5)

    return 0

try:
    # 없는 모듈 import시 에러 발생
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
except:
    print("selenium 모듈을 설치합니다.")
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'selenium'])
    
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options

try:
    from webdriver_manager.chrome import ChromeDriverManager
except:
    print("webdriver-manager 모듈을 설치합니다.")
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'webdriver-manager'])
    
    from webdriver_manager.chrome import ChromeDriverManager

try:
    from openpyxl import Workbook
except:
    print("openpyxl 모듈을 설치합니다.")
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'openpyxl'])
    
    from openpyxl import Workbook


try:
    import pandas as pd
except:
    print("pandas 모듈을 설치합니다.")
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pandas'])
    
    import pandas as pd

try:
    from bs4 import BeautifulSoup
except:
    print("bs4 모듈을 설치합니다.")
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'bs4'])
    from bs4 import BeautifulSoup

try:
    from konlpy.tag import Okt
except:
    print("konlpy 모듈을 설치합니다.")
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'konlpy'])
    from konlpy.tag import Okt



    # 인급동 xpath
    # /html/body/ytd-app/div[1]/tp-yt-app-drawer/div[2]/div/div[2]/div[2]/ytd-guide-renderer/div[1]/ytd-guide-section-renderer[3]/div/ytd-guide-entry-renderer[1]/a

try:
    # 접속 url
    keywordurl = 'https://trends.google.co.kr/trends/trendingsearches/daily?geo=KR&hl=ko'
    url = "https://youtube.com/"

    
    # 크롬 드라이버 매니저 연결
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=Options())
    # 윈도우 전체화면으로 실행
    driver.maximize_window()

    # 구글 데일리 인기 검색어 1위 키워드 추출 후 키워드로 입력
    driver.get(keywordurl)
    driver.implicitly_wait(10)
    # keyword = driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div[1]/ng-include/div/div/div/div/md-list[1]/feed-item/ng-include/div/div/div[1]/div[2]/div[1]/div/span/a').text
    keyword = "두간"
    # 유튜브 접속
    driver.get(url)
    driver.implicitly_wait(10)

    # 키워드 입력하여 검색
    search = driver.find_element(By.NAME,"search_query")
    search.send_keys(keyword + ' -Shorts')
    search.send_keys(Keys.ENTER)

    driver.implicitly_wait(10)

    # 반복 시작-------------------------------------------

    # 영상 클릭
    xpath = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{}]/div[1]'.format(1)
    contents = driver.find_element(By.XPATH,xpath)
    driver.implicitly_wait(10)

    contents.click()
    driver.implicitly_wait(10)

    # 영상 일시정지
    driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[1]/video').click()
    driver.implicitly_wait(10)

    # 영상 설명 더보기 클릭
    driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[3]/div[1]').click()
    driver.implicitly_wait(10)

    video_info = info_collect(driver) # 영상 정보를 json형태로 리턴 받음

    for key, value in video_info.items():
        print(key+" : "+value)

    print("스크롤 시작 :" + time.strftime('%H.%M.%S'))
    scroll_down(driver)
    
    print("대댓글 열기 시작 :" + time.strftime('%H.%M.%S'))
    open_reply(driver)
    print("대댓글 열기 종료 :" + time.strftime('%H.%M.%S'))

except Exception as e:
    print(e)