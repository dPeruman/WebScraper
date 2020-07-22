from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
#import requests
#from urllib.request import urlopen
#from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time

"""
This code is scrape data from linkedin.com

"""
## Download the chromedriver from : https://chromedriver.chromium.org/
## And give the location of executable here
PATH  = "/chromedriver.exe"
driver = webdriver.Chrome(PATH)

def linkedin_scraper(dataframe,sk='ai', loc='bangalore'):
    """This function scrapes data from linkedin.com

    Args:

        sk (str, optional): [skill]. Defaults to 'ai'.
        loc (str, optional): [loaction]. Defaults to 'bangalore'.
    """

    sk = sk #skill
    loc = loc #location
    url = 'https://www.linkedin.com/jobs/'

    driver.get(url)
    driver.implicitly_wait(4)

    driver.find_element_by_css_selector('#JOBS > section.dismissable-input.typeahead-input.location-typeahead-input > button > icon > svg').click()
    loc_input = driver.find_element_by_css_selector('#JOBS > section.dismissable-input.typeahead-input.location-typeahead-input > input')
    #loc_input.click()
    loc_input.send_keys(loc)
    loc_input.send_keys(Keys.SHIFT, Keys.TAB)
    job_input = driver.find_element_by_css_selector('#JOBS > section.dismissable-input.typeahead-input.keywords-typeahead-input > input')
    job_input.send_keys(sk)
    #job_input.send_keys(Keys.TAB)
    #job_input.send_keys(Keys.TAB)
    #time.sleep(3)
    

    job_input.submit()
    driver.implicitly_wait(4)
    #time.sleep(5)
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    count = 0

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(1)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            if(count <= 2):
                try:
                    see_more = driver.find_element_by_css_selector('#main-content > div > section > button')
                    see_more.click()
                    count = count+1
                except :
                    break
            else:
                break
        last_height = new_height

    time.sleep(2)

    all_jobs = driver.find_elements_by_class_name('result-card')
    for job in all_jobs:

        result_html = job.get_attribute('innerHTML')
        soup = BeautifulSoup(result_html, 'html.parser')
        
        try:
            href = soup.find('a', class_='result-card__full-card-link')
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
            location = soup.find('span', class_='job-result-card__location')
            location = location.text.strip()
            #print(location)
        except:
            location = 'NaN'

        try:
            company = soup.find('a', class_="result-card__subtitle-link").text.strip()
            
        except:
            try:
                company = soup.find('h4', class_="result-card__subtitle").text.strip()
            except :
                company = 'NaN'

        skill_list = 'NaN'

        
        salary = 'NaN'

        experience = 'NaN'
        
        qualifications = 'NaN'
        
        dataframe = dataframe.append({'Recruiter name':recruiter_name, 'Recruter tel':phone_no, 'Recuiter mail id':email,
                                'Company website':web_, 'Job location':location, 'Company name':company,
                                'Skill set required':skill_list, 'Description url':desc_url, 'Salary offered':salary,
                                'Experience required':experience, 'Qualification required':qualifications},ignore_index=True)
        
        


    driver.close()
    return dataframe
    #dataframe.to_csv("linkedin.csv",index=False)


if(__name__=='__main__'):
    
    dataframe = pd.DataFrame(columns = ['Recruiter name', 'Recruter tel', 'Recuiter mail id',
                                        'Company website', 'Job location', 'Company name',
                                        'Skill set required', 'Description url', 'Salary offered',
                                        'Experience required', 'Qualification required'])

    linkedin_scraper(dataframe) #calls linkedin_scraper method


