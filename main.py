import naukri2
import monster
import indeed
import times_jobs
import shine
import linkedin 
import pandas as pd


"""This takes info from user and returns scraped data from Naukri, monster, indeed, timejobs, shine and linkedin
"""

## Download the chromedriver from : https://chromedriver.chromium.org/
## And give the location of executable here

PATH = 'C:\\Users\\DHEERAJ SKYLARK\\Downloads\\chromedriver_win32\\chromedriver.exe'

naukri2.PATH = monster.PATH = indeed.PATH = times_jobs.PATH = shine.PATH = linkedin.PATH = PATH



def main(dataframe):
    skill = input('Enter a skill: ')
    location = input('Enter location: ')
    experience = int(input('Enter experience in years: '))

    dataframe = naukri2.naukri_scraper(dataframe, sk=skill, exp=experience, loc=location)
    dataframe = monster.monster_scraper(dataframe, sk=skill, exp=experience, loc=location)
    #dataframe = indeed.indeed_scraper(dataframe, sk=skill, exp=experience, loc=location)
    #dataframe = times_jobs.timesJobs_scraper(dataframe, sk=skill, exp=experience, loc=location)
    #dataframe = shine.shine_scraper(dataframe, sk=skill, exp=experience, loc=location)
    #dataframe = linkedin.linkedin_scraper(dataframe, sk=skill, loc=location)

    dataframe.to_csv("Jobs.csv",index=False)

if __name__ == '__main__':

    dataframe = pd.DataFrame(columns = ['Recruiter name', 'Recruter tel', 'Recuiter mail id',
                                        'Company website', 'Job locaion', 'Company name',
                                        'Skill set required', 'Description url', 'Salary offered',
                                        'Experience required', 'Qualification required'])

    main(dataframe)