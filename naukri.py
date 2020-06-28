from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup

## Download the chromedriver from link in description
## And give the location of executable here
driver = webdriver.Chrome("C:\\Users\\DHEERAJ SKYLARK\\Downloads\\chromedriver_win32\\chromedriver.exe")

dataframe = pd.DataFrame(columns = ['Recruiter name', 'Recruter tel', 'Recuiter mail id',
                                     'Company website', 'Job locaion', 'Company name',
                                     'Skill set required', 'Description url', 'Salary offered',
                                     'Experience required', 'Qualification required'])
sk = 'ai'#skill
exp = 'experience='+str(3)# experience
loc = 'bangalore'
#https://www.naukri.com/ai-jobs-in-bangalore-2?experience=5

for i in range(1,3):

        if(i == 1):
        ##Step1: Get the page
            url = 'https://www.naukri.com/'+sk+'-jobs-in-'+loc+'?'+exp
        else:
            url = 'https://www.naukri.com/'+sk+'-jobs-in-'+loc+'-'+str(i)+'?'+exp
        #url = 'https://www.naukri.com/ai-jobs-in-bangalore?experience=11'
        driver.get(url)#TODO make it generic
        driver.implicitly_wait(4)

        all_jobs = driver.find_elements_by_class_name('jobTuple')
        print(all_jobs)
        for job in all_jobs:

            result_html = job.get_attribute('innerHTML')
            soup = BeautifulSoup(result_html,'html.parser')
            try:
                href = soup.find('a', class_='title')
                href = href['href']
                desc_url = href
                #driver.execute_script("window.open('');")
                #driver.switch_to.window(driver.window_handles[1])
                #driver.get(href)
                #print(href)
                #driver.close()
                #driver.switch_to.window(driver.window_handles[0])
                #details = driver.find_elements_by_class_name('jd-container')[0]
                #soup2 = BeautifulSoup(details.get_attribute('innerHTML'), 'html.parser')
                #f1 = open('soup2.html', 'w')
                #f1.write(soup2.text)
                #f1.close()
            except :
                href = 'None'
                desc_url = 'None'
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
                    recruiter_name = 'None'
                
                if(labels_original[1] in labels):
                    Index = labels.index(labels_original[1])
                    phone_no = temp[Index]
                else:
                    phone_no = 'None'
            
                if(labels_original[2] in labels):
                    Index = labels.index(labels_original[2])
                    email = temp[Index]
                else:
                    email = 'None'
                
                if(labels_original[3] in labels):
                    Index = labels.index(labels_original[3])
                    web_ = temp[Index]
                else:
                    web_ = 'None'
                del(labels,temp,x,y)
            except :
                recruiter_name = 'None'
                phone_no = 'None'
                email = 'None'
                web_ = 'None'
            
            try:
                skills = soup.findAll('li', class_='fleft fs12 grey-text lh16 dot')
                #print(skills[0].text)
                skill_list = [x.text for x in skills]
            except:
                skill_list = 'None'

            try:
                location = soup.find('li',class_='location')
                location = location.span['title'].strip()
                #print(location)
            except:
                location = 'None'

            try:
                company = soup.find('div', class_="companyInfo").a.text.strip()
            except:
                company = 'None'

            try:
                salary = soup.find('li', class_="salary").span.text.strip()
                if(salary == 'Not disclosed'):
                    salary = 'None'
            except:
                salary = 'None'
            
            try:
                experience = soup.find('li', class_='experience').span.text.strip()
            except :
                experience = 'None'

            try:
                1/0
                qualifications = soup2.findAll('div', class_='details')
                level = []
                quals = []
                for i in qualifications:
                    if(i.label.text == 'PG :' or i.label.text == 'UG :' or i.label.text == 'Doctorate :'):
                        level.append(i.label.text)
                        quals.append(i.span.text)
                qualifications = dict(zip(level,quals))

                print(qualifications)
                

            except :
                qualifications = 'None'
            #driver.close()
            #driver.switch_to.window(driver.window_handles[0])

            dataframe = dataframe.append({'Recruiter name':recruiter_name, 'Recruter tel':phone_no, 'Recuiter mail id':email,
                                     'Company website':web_, 'Job locaion':location, 'Company name':company,
                                     'Skill set required':skill_list, 'Description url':desc_url, 'Salary offered':salary,
                                     'Experience required':experience, 'Qualification required':qualifications},ignore_index=True)

driver.close()
dataframe.to_csv("naukri.csv",index=False)