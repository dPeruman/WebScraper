from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen

## Download the chromedriver from : https://chromedriver.chromium.org/
## And give the location of executable here
PATH = "/chromedriver.exe"
driver = webdriver.Chrome(PATH)

def monster_scraper(dataframe, sk='ai', exp=3, loc='bangalore'):
    """
    This function scrapes data from monsterindia.com

    Args:
        
        sk (str, optional): [skill]. Defaults to 'ai'.
        exp (int, optional): [experience]. Defaults to 3.
        loc (str, optional): [loaction]. Defaults to 'bangalore'.
    """
    
    sk = sk #skill
    exp = str(exp) # experience
    loc = loc #location

    for i in range(0,2000,100):

            if(i == 0):
            ##Step1: Get the page
                url = 'https://www.monsterindia.com/srp/results?sort=1&limit=100&query='+sk+'&locations='+loc+'&experienceRanges='+exp+'~'+exp+'&experience='+exp
            else:
                url = 'https://www.monsterindia.com/srp/results?start='+str(i)+'&sort=1&limit=100&query='+sk+'&locations='+loc+'&experienceRanges='+exp+'~'+exp+'&experience='+exp
            #source = urlopen(url)
            #soup = BeautifulSoup(source, 'html.parser')
            #all_jobs = soup.findAll('div', class_='card-body')
            driver.get(url)#TODO make it generic
            driver.implicitly_wait(4)
            if(i == 0):
                limit = driver.find_elements_by_class_name('main-heading')[1].text
                limit = int(limit[17:])
            all_jobs = driver.find_elements_by_class_name('card-body-apply')
            #print(all_jobs)
            for job in all_jobs:

                result_html = job.get_attribute('innerHTML')
                soup = BeautifulSoup(result_html, 'html.parser')
                try:
                    href = soup.find('div', class_='job-tittle')
                    href = href.h3.a['href']
                    desc_url = href

                    """
                    #TODO 1. un-comment this block of lines to get recruiter details, but it is very slow to get the details.
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(href)
                    details = driver.find_elements_by_class_name('jd-container')[0]
                    soup2 = BeautifulSoup(details.get_attribute('innerHTML'), 'html.parser')

                    """

                
                except:
                    href = 'NaN'
                    desc_url = 'NaN'

                """
                #Use this block to write code for scraping details for: recruiter_name, phone_no, email, web_
                try:
                    1/0
                    complete_info = soup2.findAll('div', class_='comp-info-detail')
                    print(complete_info)
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
                    print(labels)
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
                except:
                    recruiter_name = 'NaN'
                    phone_no = 'NaN'
                    email = 'NaN'
                    web_ = 'NaN'
                """
                recruiter_name = 'NaN'
                phone_no = 'NaN'
                email = 'NaN'
                web_ = 'NaN'

                try:
                    location = soup.find('span',class_='loc')
                    location = location.small.text.strip()
                    #print(location)
                except:
                    location = 'NaN'

                try:
                    company = soup.find('span', class_="company-name").a.text.strip()
                except:
                    company = 'NaN'

                try:
                    skills = soup.findAll('span', class_='grey-link')
                    #print(skills[0].text)
                    skill_list = [x.a.text.replace(',','').strip() for x in skills]
                except:
                    skill_list = 'NaN'

                try:
                    salary = soup.find('div', class_ = 'package').span.small.text.replace(',','').strip()
                    if(salary == 'Not Specified'):
                        salary = 'NaN'
                except:
                    salary = 'NaN'

                try:
                    experience = soup.find('div', class_='exp').span.small.text.replace(',','').strip()
                except:
                    experience = 'NaN'
                """
                try:
                    #Use this block to write code for scraping qualification details
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
                    

                except:
                    qualifications = 'NaN'
                #driver.close()
                #driver.switch_to.window(driver.window_handles[0])

                """
                qualifications = 'NaN'
                
                dataframe = dataframe.append({'Recruiter name':recruiter_name, 'Recruter tel':phone_no, 'Recuiter mail id':email,
                                        'Company website':web_, 'Job location':location, 'Company name':company,
                                        'Skill set required':skill_list, 'Description url':desc_url, 'Salary offered':salary,
                                        'Experience required':experience, 'Qualification required':qualifications},ignore_index=True)
            
            if((i+100) >= limit):
                break
    driver.close()
    return dataframe
    #dataframe.to_csv("monster.csv",index=False)


if(__name__=='__main__'):

    dataframe = pd.DataFrame(columns = ['Recruiter name', 'Recruter tel', 'Recuiter mail id',
                                        'Company website', 'Job location', 'Company name',
                                        'Skill set required', 'Description url', 'Salary offered',
                                        'Experience required', 'Qualification required'])

    monster_scraper(dataframe)

