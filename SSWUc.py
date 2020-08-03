# from urllib.request import urlopen
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys, os
import getpass
import time
"""
import tkinter

window = tkinter.Tk()
window.mainloop()
window.title("iSSWU")
window.geometry('800x800+50+50')
"""
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("lang=ko_KR")

# UserAgent값을 바꿔줍시다!
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

driver = webdriver.Chrome("./chromedriver",options = options)
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
driver.get('https://lms.sungshin.ac.kr/ilos/main/member/login_form.acl')
'''
#입력 받는 곳
label = tkinter.Label(window,text="아이디")
label.grid(column=1, row=0)
id1 = tkinter.Entry(window, width=20)
id1.grid(column=1, row=0)
def clicked():
    res = "id : "+id1.get()
    label.configure(text=res, fg="red")
bt = tkinter.Button(window, text="Enter", command=clicked)
bt.grid(column=1, row=1)

window.mainloop()
'''
print("성신교육시스템 접속")
user_id = input('아이디 : ')
user_pwd = getpass.getpass('비밀번호 : ')
driver.find_element_by_id('usr_id').send_keys(user_id)
driver.find_element_by_id('usr_pwd').send_keys(user_pwd)
driver.find_element_by_id('login_btn').click()

#find_elements_by_css_selector
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sub_open')))
size = len(driver.find_elements_by_class_name('sub_open'))
print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
print('                          아직 못들은 강의                         ')
print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
print('      과목명        |       강의명       |  진도율 |  마감일까지 |')
#과목 하나씩 들락날락
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
     #진행활동 엔트리 하나하나에 접근    
    for entry in range(listsize):
        submainRight = driver.find_elements_by_css_selector('div.submain-right > div.submain-noticebox')
        inglist = submainRight[0].find_elements_by_css_selector('div.submain-noticebox > ol > li')
        subject = driver.find_element_by_id('subject-span').text
        lec_name = inglist[entry].find_element_by_css_selector('li > em > a').text
        #진행활동에 있는 엔트리가 온라인 강의면 
        if '온라인 강의' in lec_name :
            lec_no = int(lec_name[lec_name.index('차시')-1]) #강의 차수 추출
            dday = inglist[entry].find_element_by_css_selector('li > span').text #d-day 추출(미리)
            inglist[entry].find_element_by_css_selector('li > em > a').click() #해당 차시 강의 클릭
#             time.sleep(0.3)
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
#과제
"""
print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
print('                          아직 못 끝낸 과제                          ')
print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
print('      과목명        |       과제명       |  제출여부  |  마감일까지 |')
driver.find_element_by_id('show_schedule_list').click()
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'site-link')))

tasknamelist = driver.find_elements_by_class_name('schedule-show-control schedule_view_list_box')
listsize = len(tasknamelist)
for s in range(listsize):
    taskddaylist = driver.find_elements_by_css_selector('span.schedule_view_title')
    tasknamelist = driver.find_elements_by_class_name('schedule-show-control schedule_view_list_box')
    subjects = driver.find_elements_by_css_selector('div.schedule_view_title')
    if taskddaylist[s].text == '종료':
        break;
    taskstates = driver.find_elements_by_css_selector('div.schedule_view_txt')
    if taskstates[s*2].text == '미제출':
        print((subjects[s].split('('))[0].ljust(13), (tasknamelist.split(']'))[1].rjust(12),'      ',
                      taskstates[s*2].text.rjust(3), '      ', taskddaylist[s].rjust(4))
print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
"""
user_id = ''
user_pwd = ''
driver.quit()
      # print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
    
