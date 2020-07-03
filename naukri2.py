from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen

## Download the chromedriver from : https://chromedriver.chromium.org/
## And give the location of executable here
PATH = "./chromedriver.exe"
driver = webdriver.Chrome(PATH)
def naukri_scraper(dataframe, sk='ai', exp=3, loc='bangalore'):
    """This function scrapes data from naukri.com

    Args:
        dataframe (pandas dataframe): [it stores the data]
        sk (str, optional): [skill]. Defaults to 'ai'.
        exp (int, optional): [experience]. Defaults to 3.
        loc (str, optional): [loaction]. Defaults to 'bangalore'.
    """    
    sk = sk #skill
    exp = 'experience='+str(exp) # experience
    loc = loc #location

    for i in range(1,1000):

            if(i == 1):
            ##Step1: Get the page
                url = 'https://www.naukri.com/'+sk+'-jobs-in-'+loc+'?'+exp
            else:
                url = 'https://www.naukri.com/'+sk+'-jobs-in-'+loc+'-'+str(i)+'?'+exp
            #url = 'https://www.naukri.com/ai-jobs-in-bangalore?experience=11'
            driver.get(url)#TODO make it generic
            driver.implicitly_wait(4)
            if(i == 1):
                limit = driver.find_element_by_class_name('sortAndH1Cont')
                limit = int(limit.text.replace(' ',',').replace('\n',',').split(',')[4])/20
            all_jobs = driver.find_elements_by_class_name('jobTuple')
            #print(all_jobs)
            for job in all_jobs:

                result_html = job.get_attribute('innerHTML')
                soup = BeautifulSoup(result_html,'html.parser')
                try:
                    href = soup.find('a', class_='title')
                    href = href['href']
                    desc_url = href
                    
                    """
                    #TODO 1. un-comment this block of lines to get recruiter details, but it is very slow to get the details.
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(href)
                    details = driver.find_elements_by_class_name('jd-container')[0]
                    soup2 = BeautifulSoup(details.get_attribute('innerHTML'), 'html.parser')

                    """

                except :
                    href = 'NaN'
                    desc_url = 'NaN'
                try:
                    1/0 #TODO 2. remove this line, when todo 1 is done.
                    complete_info = soup2.findAll('div', class_='comp-info-detail')
                    #print(complete_info)
                    labels = []#to store labels
                    temp = []
                    for i in complete_info:
                        x = i.label.text
                        labels.append(x)
                        if(x == 'Website'):
                            y = i.span.a.text
                            temp.append(y)
                        else:
                            y = i.span.text
                            temp.append(y)
                    #print(labels)
                    labels_original = ['Contact Person', 'Phone Number', 'Email', 'Website']
                    
                    if(labels_original[0] in labels):
                        Index = labels.index(labels_original[0])
                        recruiter_name = temp[Index]
                    else:
                        recruiter_name = 'NaN'

                    if(labels_original[1] in labels):
                        Index = labels.index(labels_original[1])
                        phone_no = temp[Index]
                    else:
                        phone_no = 'NaN'
                
                    if(labels_original[2] in labels):
                        Index = labels.index(labels_original[2])
                        email = temp[Index]
                    else:
                        email = 'NaN'

                    if(labels_original[3] in labels):
                        Index = labels.index(labels_original[3])
                        web_ = temp[Index]
                    else:
                        web_ = 'NaN'
                    del(labels,temp,x,y)
                except :
                    recruiter_name = 'NaN'
                    phone_no = 'NaN'
                    email = 'NaN'
                    web_ = 'NaN'
                try:
                    location = soup.find('li',class_='location')
                    location = location.span['title'].strip()
                    #print(location)
                except:
                    location = 'NaN'

                try:
                    company = soup.find('div', class_="companyInfo").a.text.strip()
                except:
                    company = 'NaN'

                try:
                    skills = soup.findAll('li', class_='fleft fs12 grey-text lh16 dot')
                    #print(skills[0].text)
                    skill_list = [x.text for x in skills]
                except:
                    skill_list = 'NaN'

                try:
                    salary = soup.find('li', class_="salary").span.text.strip()
                    if(salary == 'Not disclosed'):
                        salary = 'NaN'
                except:
                    salary = 'NaN'

                try:
                    experience = soup.find('li', class_='experience').span.text.strip()
                except :
                    experience = 'NaN'

                try:
                    1/0 # TODO 3. comment this line of todo 1 and todo 2 are done
                    qualifications = soup2.findAll('div', class_='details')
                    level = []
                    quals = []
                    for i in qualifications:
                        if(i.label.text == 'PG :' or i.label.text == 'UG :' or i.label.text == 'Doctorate :'):
                            level.append(i.label.text)
                            quals.append(i.span.text)
                    qualifications = dict(zip(level,quals))
                    del(level,quals)

                    #print(qualifications)
                    

                except :
                    qualifications = 'NaN'
                #driver.close()
                #driver.switch_to.window(driver.window_handles[0])

                dataframe = dataframe.append({'Recruiter name':recruiter_name, 'Recruter tel':phone_no, 'Recuiter mail id':email,
                                        'Company website':web_, 'Job locaion':location, 'Company name':company,
                                        'Skill set required':skill_list, 'Description url':desc_url, 'Salary offered':salary,
                                        'Experience required':experience, 'Qualification required':qualifications},ignore_index=True)
            if(i >= limit):
                break

    driver.close()
    dataframe.to_csv("naukri.csv",index=False)


if(__name__=='__main__'):
    dataframe = pd.DataFrame(columns = ['Recruiter name', 'Recruter tel', 'Recuiter mail id',
                                        'Company website', 'Job locaion', 'Company name',
                                        'Skill set required', 'Description url', 'Salary offered',
                                        'Experience required', 'Qualification required'])

    naukri_scraper(dataframe)

