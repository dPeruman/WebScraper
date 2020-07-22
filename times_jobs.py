from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen

## Download the chromedriver from : https://chromedriver.chromium.org/
## And give the location of executable here
PATH = "/chromedriver.exe"
driver = webdriver.Chrome(PATH)

def timesJobs_scraper(dataframe, sk='ai', exp=3, loc='bangalore'):
    """This function scrapes data from timesjobs.com

    Args:
    
        sk (str, optional): [skill]. Defaults to 'ai'.
        exp (int, optional): [experience]. Defaults to 3.
        loc (str, optional): [loaction]. Defaults to 'bangalore'.
    """
    
    sk = sk #skill
    exp = str(exp) # experience
    loc = loc #location
#https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=ai&txtLocation=Bangalore&luceneResultSize=100&postWeek=60&txtKeywords=ai&cboWorkExp1=3&pDate=I&sequence=1&startPage=1
    for i in range(1,1000):

            url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&actualTxtKeywords='+sk+'&txtLocation='+loc+'&luceneResultSize=100&pstWeek=60&txtKeywords='+sk+'&cboWorkExp1='+exp+'&pDate=I&sequence='+str(i)+'&startPage=1'
            #source = urlopen(url)
            #soup = BeautifulSoup(source, 'html.parser')
            #all_jobs = soup.findAll('div', class_='card-body')
            driver.get(url)#TODO make it generic
            driver.implicitly_wait(4)
            if(i == 1):
                limit = driver.find_element_by_id('totolResultCountsId').text
                limit = int(limit)/100
            all_jobs = driver.find_elements_by_class_name('job-bx')
            #print(all_jobs)
            for job in all_jobs:

                result_html = job.get_attribute('innerHTML')
                soup = BeautifulSoup(result_html, 'html.parser')
                try:
                    href = soup.find('a')
                    href = href['href']
                    desc_url = href

                
                except:
                    href = 'NaN'
                    desc_url = 'NaN'

                
                recruiter_name = 'NaN'
                phone_no = 'NaN'
                email = 'NaN'
                web_ = 'NaN'

                try:
                    location = soup.find('ul', class_='clearfix').findAll('li')[1]
                    location = location.span['title'].strip()
                    #print(location)
                except:
                    location = 'NaN'

                try:
                    company = soup.find('h3', class_="joblist-comp-name")
                    if(company.span):
                        company = company.text.replace('(More Jobs)', " ").strip()
                    else:
                        company = company.text.strip()
                except:
                    company = 'NaN'

                try:
                    skills = soup.find('span', class_='srp-skills')
                    #print(skills[0].text)
                    skill_list = skills.text.strip().replace('  ,  ', ',').split(',')
                except:
                    skill_list = 'NaN'

                
                salary = 'NaN'

                try:
                    experience = soup.find('ul', class_='clearfix').findAll('li')[0]
                    experience = experience.text[11:]
                except:
                    experience = 'NaN'
                
                qualifications = 'NaN'
                
                dataframe = dataframe.append({'Recruiter name':recruiter_name, 'Recruter tel':phone_no, 'Recuiter mail id':email,
                                        'Company website':web_, 'Job location':location, 'Company name':company,
                                        'Skill set required':skill_list, 'Description url':desc_url, 'Salary offered':salary,
                                        'Experience required':experience, 'Qualification required':qualifications},ignore_index=True)
            
            if(i >= limit):
                break
    driver.close()
    return dataframe
    #dataframe.to_csv("timesJobs.csv",index=False)


if(__name__=='__main__'):
    dataframe = pd.DataFrame(columns = ['Recruiter name', 'Recruter tel', 'Recuiter mail id',
                                        'Company website', 'Job location', 'Company name',
                                        'Skill set required', 'Description url', 'Salary offered',
                                        'Experience required', 'Qualification required'])

    timesJobs_scraper(dataframe)


