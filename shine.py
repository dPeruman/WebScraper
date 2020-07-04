from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from selenium.webdriver.support.ui import Select
import time

## Download the chromedriver from : https://chromedriver.chromium.org/
## And give the location of executable here
PATH = "./chromedriver.exe"
driver = webdriver.Chrome(PATH)

def shine_scraper(sk='ai', exp=3, loc='bangalore'):
    """This function scrapes data from timesjobs.com

    Args:
        
        sk (str, optional): [skill]. Defaults to 'ai'.
        exp (int, optional): [experience]. Defaults to 3.
        loc (str, optional): [loaction]. Defaults to 'bangalore'.
    """
    dataframe = pd.DataFrame(columns = ['Recruiter name', 'Recruter tel', 'Recuiter mail id',
                                        'Company website', 'Job locaion', 'Company name',
                                        'Skill set required', 'Description url', 'Salary offered',
                                        'Experience required', 'Qualification required'])

    sk = sk #skill
    if(exp > 24):
        exp = str(exp)+'+ Yrs'
    else:
        exp = str(exp)+' Yrs'#experience

    loc = loc #location
    url = 'https://www.shine.com/job-search/'

    driver.get(url)
    driver.implicitly_wait(4)

    button = driver.find_element_by_id('id_searchButton')
    button.click()
    job_input = driver.find_element_by_id('id_q')
    loc_input = driver.find_element_by_id('id_loc')
    exp_input = Select(driver.find_element_by_id('id_minexp'))

    job_input.send_keys(sk)
    loc_input.send_keys(loc)
    exp_input.select_by_visible_text(exp)


    job_input.submit()
    driver.implicitly_wait(4)
    time.sleep(5)
    print(driver.current_url)

    try:
        close = driver.find_element_by_css_selector('#id_registerPopModalCancel > span')#to close pop up if any
        close.click()
    except :
        pass
    try:
        close_noti = driver.find_element_by_css_selector('#push_noti_popup > div.js-msg-parent > span')
        close_noti.click()
    except :
        pass            

#https://www.shine.com/job-search/ai-jobs-in-bangalore-3?loc=Bangalore&minexp=4
    for i in range(1,1000):
            
            try:
                close = driver.find_element_by_css_selector('#id_registerPopModalCancel > span')#to close pop up if any
                close.click()
            except :
                pass
            
            all_jobs = driver.find_elements_by_class_name('result-display__profile')
            length = len(all_jobs)
            temp = temp+length
            #print(all_jobs)
            for job in all_jobs:

                result_html = job.get_attribute('innerHTML')
                soup = BeautifulSoup(result_html, 'html.parser')
                button = job.find_element_by_class_name('job_title_anchor')
                try:
                    button.click()
                except:
                    close = driver.find_element_by_css_selector('#id_registerPopModalCancel > span')#to close pop up if any
                    close.click()
                    button.click()
                    #pass
                try:
                    href = soup.find('a', class_='job_title_anchor')
                    href = href['href']
                    desc_url = 'https://www.shine.com'+href

                
                except:
                    href = 'NaN'
                    desc_url = 'NaN'

                
                recruiter_name = 'NaN'
                phone_no = 'NaN'
                email = 'NaN'
                web_ = 'NaN'

                try:
                    location = soup.findAll('li', class_='result-display__profile__years')[1]
                    location = location.text.strip()
                    #print(location)
                except:
                    location = 'NaN'

                try:
                    company = soup.find('ul', class_="justify-content-between").li.span.text.strip()
                    
                except:
                    company = 'NaN'

                try:
                    skills = driver.find_elements_by_class_name('key_skills__skill')
                    #print(skills[0].text)
                    skill_list = [x.text.strip() for x in skills]
                except:
                    try:
                        close = driver.find_element_by_css_selector('#id_registerPopModalCancel > span')#to close pop up if any
                        close.click()
                        skills = driver.find_elements_by_class_name('key_skills__skill')
                        #print(skills[0].text)
                        skill_list = [x.text.strip() for x in skills]

                    except:
                        skill_list = 'NaN'

                
                salary = 'NaN'

                try:
                    experience = soup.find('li', class_='result-display__profile__years')
                    experience = experience.text.strip()
                except:
                    experience = 'NaN'
                
                qualifications = 'NaN'
                
                dataframe = dataframe.append({'Recruiter name':recruiter_name, 'Recruter tel':phone_no, 'Recuiter mail id':email,
                                        'Company website':web_, 'Job locaion':location, 'Company name':company,
                                        'Skill set required':skill_list, 'Description url':desc_url, 'Salary offered':salary,
                                        'Experience required':experience, 'Qualification required':qualifications},ignore_index=True)
                
            try:
                next = driver.find_elements_by_class_name('pagination_button')[-1]
                next.click()#next page
            except :
                try:
                    close = driver.find_element_by_css_selector('#id_registerPopModalCancel > span')#to close pop up if any
                    close.click()
                    next = driver.find_elements_by_class_name('pagination_button')[-1]
                    next.click()
                except :
                    break#if no next page is available loop breaks



    driver.close()
    dataframe.to_csv("shine.csv",index=False)


if(__name__=='__main__'):
    
    shine_scraper()#calls shine method


