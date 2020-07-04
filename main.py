from shine import shine_scraper
from monster import monster_scraper
from times_jobs import timesJobs_scraper
from indeed import indeed_scraper
from naukri2 import naukri_scraper
from linkedin import linkedin_scraper

"""This takes info from user and returns scraped data from Naukri, monster, indeed, timejobs, shine and linkedin
"""

def main():
    skill = input('Enter a skill')
    location = input('Enter location')
    experience = int(input('Enter experience in years'))

    naukri_scraper(sk=skill, exp=experience, loc=location)
    monster_scraper(sk=skill, exp=experience, loc=location)
    indeed_scraper(sk=skill, exp=experience, loc=location)
    timesJobs_scraper(sk=skill, exp=experience, loc=location)
    shine_scraper(sk=skill, exp=experience, loc=location)
    linkedin_scraper(sk=skill, loc=location)

    

if __name__ == '__main__':
    main()