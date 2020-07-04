import naukri2
import monster
import indeed
import times_jobs
import shine
import linkedin


"""This takes info from user and returns scraped data from Naukri, monster, indeed, timejobs, shine and linkedin
"""

## Download the chromedriver from : https://chromedriver.chromium.org/
## And give the location of executable here

PATH = './chromedriver.exe'

naukri2.PATH = monster.PATH = indeed.PATH = times_jobs.PATH = shine.PATH = linkedin.PATH = PATH\

def main():
    skill = input('Enter a skill')
    location = input('Enter location')
    experience = int(input('Enter experience in years'))

    naukri2.naukri_scraper(sk=skill, exp=experience, loc=location)
    monster.monster_scraper(sk=skill, exp=experience, loc=location)
    indeed.indeed_scraper(sk=skill, exp=experience, loc=location)
    times_jobs.timesJobs_scraper(sk=skill, exp=experience, loc=location)
    shine.shine_scraper(sk=skill, exp=experience, loc=location)
    linkedin.linkedin_scraper(sk=skill, loc=location)

    

if __name__ == '__main__':
    main()