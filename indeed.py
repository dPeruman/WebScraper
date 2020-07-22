from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen

## Download the chromedriver from : https://chromedriver.chromium.org/
## And give the location of executable here
PATH = "/chromedriver.exe"
driver = webdriver.Chrome(PATH)

def indeed_scraper(dataframe, sk='ai', exp=3, loc='bangalore'):
    """This function scrapes data from indeed.com

    Args:
        
        sk (str, optional): [skill]. Defaults to 'ai'.
        exp (int, optional): [experience]. Defaults to 3.
        loc (str, optional): [loaction]. Defaults to 'bangalore'.
    """
    
    sk = sk #skill
    exp = str(exp) # experience
    loc = loc #location
    temp = 0
# ! https://www.indeed.co.in/jobs?q=ai&l=Bangalore&start=10
    for i in range(0,40,10):

            url = 'https://www.indeed.co.in/jobs?q='+sk+'&l='+loc+'&start='+str(i)
            #source = urlopen(url)
            #soup = BeautifulSoup(source, 'html.parser')
            #all_jobs = soup.findAll('div', class_='card-body')
            c = driver.get(url)#TODO make it generic
            driver.implicitly_wait(4)
            if(i == 0):
                limit = int(driver.find_element_by_id('searchCountPages').text.split(' ')[3])
            all_jobs = driver.find_elements_by_class_name('jobsearch-SerpJobCard')
            length = len(all_jobs)
            temp = temp+length
            #print(all_jobs)
            for job in all_jobs:

                result_html = job.get_attribute('innerHTML')
                soup = BeautifulSoup(result_html, 'html.parser')
                try:
                    href = soup.find('h2', class_='title').a
                    href = href['href']
                    desc_url = 'https://www.indeed.co.in'+href

                
                except:
                    href = 'NaN'
                    desc_url = 'NaN'

                
                recruiter_name = 'NaN'
                phone_no = 'NaN'
                email = 'NaN'
                web_ = 'NaN'

                try:
                    location = soup.find('div', class_='location').text.strip()
                    #location = location.span['title'].strip()
                    #print(location)
                except:
                    location = 'NaN'

                try:
                    company = soup.find('span', class_="company").text.strip()
                except:
                    company = 'NaN'

                skill_list = "NaN"
                
                try:
                    salary = soup.find('span', class_='salaryText').text
                except :
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
            
            if(temp >= limit):
                break
    driver.close()
    return dataframe
    #dataframe.to_csv("indeed.csv",index=False)


if(__name__=='__main__'):

    dataframe = pd.DataFrame(columns = ['Recruiter name', 'Recruter tel', 'Recuiter mail id',
                                        'Company website', 'Job location', 'Company name',
                                        'Skill set required', 'Description url', 'Salary offered',
                                        'Experience required', 'Qualification required'])

    indeed_scraper(dataframe)


