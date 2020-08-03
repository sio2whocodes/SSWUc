from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys, os
import getpass
import time

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("lang=ko_KR")

options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

driver = webdriver.Chrome("./chromedriver",options = options)
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
driver.get('https://lms.sungshin.ac.kr/ilos/main/member/login_form.acl')

print("성신교육시스템 접속")
user_id = input('아이디 : ')
user_pwd = getpass.getpass('비밀번호 : ')
driver.find_element_by_id('usr_id').send_keys(user_id)
driver.find_element_by_id('usr_pwd').send_keys(user_pwd)
driver.find_element_by_id('login_btn').click()

wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sub_open')))
size = len(driver.find_elements_by_class_name('sub_open'))
print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
print('                          아직 못들은 강의                         ')
print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
print('      과목명        |       강의명       |  진도율 |  마감일까지 |')

for s in range(size):
    #과목에 접근
    iscomplete = True;
    subjects = driver.find_elements_by_class_name('sub_open')
    subjects[s].click()
    #페이지 전환
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'site-link')))
    #진행활동에 접근
    submainRight = driver.find_elements_by_css_selector('.submain-right > .submain-noticebox')
    inglist = submainRight[0].find_elements_by_css_selector('.submain-noticebox > ol > li')
    listsize = len(inglist)
     #진행활동 엔트리에 접근    
    for entry in range(listsize):
        submainRight = driver.find_elements_by_css_selector('div.submain-right > div.submain-noticebox')
        inglist = submainRight[0].find_elements_by_css_selector('div.submain-noticebox > ol > li')
        subject = driver.find_element_by_id('subject-span').text
        lec_name = inglist[entry].find_element_by_css_selector('li > em > a').text
        
        if '온라인 강의' in lec_name :
            lec_no = int(lec_name[lec_name.index('차시')-1]) #강의 차수 추출
            dday = inglist[entry].find_element_by_css_selector('li > span').text #d-day 추출(미리)
            inglist[entry].find_element_by_css_selector('li > em > a').click() #해당 차시 강의 클릭
            #페이지 전환
            element = wait.until(EC.element_to_be_clickable((By.ID, 'per_text')))
            lecs_per = driver.find_elements_by_css_selector('#per_text') #수강 퍼센트 리스트 수집
            #해당 차시 퍼센트에 접근
            if lecs_per[lec_no-1].text != '100%' :
                iscomplete = False;
                print(((subject.split(']'))[1].split('('))[0].ljust(13), (lec_name.split(']'))[1].rjust(12),'      ',
                      lecs_per[lec_no-1].text.rjust(3), '      ', dday.rjust(4))
            driver.back()
    driver.get('http://lms.sungshin.ac.kr/ilos/main/main_form.acl')
    if iscomplete == False :
        print('-----------------------------------------------------------------')
driver.get('http://lms.sungshin.ac.kr/ilos/main/main_form.acl')

user_id = ''
user_pwd = ''
driver.quit()