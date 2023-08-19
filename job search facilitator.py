from bs4 import BeautifulSoup
import requests

# HEADER NECESSARY TO BYPASS BLOCKING FUNCTIONALITY OF CERTAIN WEBSITES
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}


# headers = {"Accept": "*/*",
# "Accept-Encoding": "gzip, deflate, br",
# "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,de;q=0.7",
# "Connection": "keep-alive",
# "Host": "baltic-job-feed-store.s3.eu-west-2.amazonaws.com",
# "If-Modified-Since": "Mon, 01 May 2023 15:03:11 GMT",
# "If-None-Match": "\"91cb3649c4e4bb37bb55b7bb147c3ea0\"",
# "Origin": "https://vacancies.balticapprenticeships.com",
# "Referer": "https://vacancies.balticapprenticeships.com/?postcode=m38%209rb&programme=Junior%20Software%20Developer%20-%20Level%203&radius=25",
# "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
# "sec-ch-ua-mobile": "?0",
# "sec-ch-ua-platform": "\"Windows\"",
# "Sec-Fetch-Dest": "empty",
# "Sec-Fetch-Mode": "cors",
# "Sec-Fetch-Site": "cross-site",
# "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36}"}
''
def retrieve_html(url):
    main_page_source = requests.get(url, headers=headers)
    soup = BeautifulSoup(main_page_source.text, "lxml")

    return soup


# ADD AN EXCLUDE KEYWORD. FOR EXAMPLE, EXCLUDE ALL RESULTS CONTAINING "DIGITAL MARKETING" OR "SENIOR"
# DATABASE CONTAINING JOBS THAT THE PROGRAM SHOULD NOT SHOW AGAIN. IF YOU IGNORE A JOB, IT SHOULD BE ADDED TO THIS DATABASE
# ENTERING PARAMETRES
print("Aaron's Job Search Facilitator! Press ^C to kill program in terminal.")
keyword = input("Enter a jobsearch keyword>").strip().lower()
postcode = input("Enter a postcode>").strip()
postcode_half1 = postcode[:3]
postcode_half2 = postcode[-3:]
distance = input("Enter distance in miles>")
keyword = "software"
distance = "40"


# CHANGE website_addresses LIST TO DICTIONARY WITH FOLLOWING FORMAT => 'findapprenticeships.gov': 'url', 'qa': 'url', etc
# PUT THE DICTIONARY IN ITS OWN FILE
# https://www.salfordcc.ac.uk/apprenticeships-salford-city-college/apprenticeshipvacancies/ WILL HAVE TO CHECK JOB TITLES MANUALLY
# https://www.nltg.co.uk/apprenticeship-vacancies/?category=14&location={postcode_half1 + postcode_hal}&radius=16
# https://www.apprentify.com/jobs/?location={postcode_half1}+{postcode_half2}&radius={distance}&salarymaximum=&keyword={keyword}
# https://uk.indeed.com/jobs?q={keyword}&l={postcode_half1}+{postcode_half2}&vjk=291938b5aa546c3e
# https://www.glassdoor.co.uk/Job/manchester-apprentice-software-developer-jobs-SRCH_IL.0,10_IC2691218_KO11,40.htm
# https://www.milkround.com/jobs/{keyword}/in-bolton?radius=10&searchOrigin=Resultlist_top-search
# https://www.alliancelearning.com/vacancies
website_addresses = {"findapprenticeships.gov": 
                     f"https://www.findapprenticeship.service.gov.uk/apprenticeships?SearchField=All&Keywords={keyword}&Location={postcode_half1}%20{postcode_half2}&WithinDistance={distance}&ApprenticeshipLevel=All&DisabilityConfidentOnly=false&Latitude=0&Longitude=0&Hash=-1210955484&SearchMode=Keyword&Category=&LocationType=NonNational&GoogleMapApiKey=0&sortType=Relevancy&SearchAction=Sort&resultsPerPage=10&DisplayDescription=true&DisplayDistance=true&DisplayClosingDate=true&DisplayStartDate=true&DisplayApprenticeshipLevel=false&DisplayWage=false",
                     "qa apprenticeships": 
                     f"https://www.qa.com/apprenticeships/apprenticeship-jobs/?category=Software%20and%20Web%20Development&postcode={postcode_half1}%20{postcode_half2}&distance={distance}&startat=0&howmany=12",
                     "baltic apprenticeships": # CANNOT SCRAPE
                     f"https://vacancies.balticapprenticeships.com/?postcode={postcode_half1}%20{postcode_half2}&programme=Junior%20Software%20Developer%20-%20Level%203&radius=25",
                     "nowskills": "https://nowskills.co.uk/apprenticeship-jobs"}

# FINDAPPRENTICESHIPS.GOV
html_text = retrieve_html(website_addresses["findapprenticeships.gov"])
job_count = 0

for job in html_text.findAll("li", class_="search-result sfa-section-bordered"):
    # if keyword not in job.div.p.text.lower():
    #     continue
    print(job.h2.a.text)  # PRINTING THE JOB TITLE)
    href = "https://www.findapprenticeship.service.gov.uk/" + job.h2.a.get("href")
    print(href)  # PRINTING URL TO SPECIFIC JOB WEB PAGE
    print(job.ul.li.text)  # PRINTING EMPLOYER
    job_page_source = requests.get(href, headers=headers)  # IN ORDER TO OBTAIN POSTCODE & APPLICATION DEADLINE
    disposable_soup = BeautifulSoup(job_page_source.text, "lxml")
    print(disposable_soup.find("p", itemprop="postalCode").text)  # PRINTING POSTCODE
    print(disposable_soup.find("p", id="vacancy-closing-date").text)  # PRINTING DEADLINE
    print()

    job_count += 1

print(f"FindApprenticeships.gov Job Count : {job_count}")


# QA APPRENTICESHIPS
html_text = retrieve_html(website_addresses["qa apprenticeships"])
job_count = 0

for job in html_text.findAll("a", class_="vacancyTile listerTile"):
    if keyword not in job.div.p.text.lower():
        continue  

    print(job.div.p.text)  # PRINTING JOB TITLE
    print(job.get("href"))  # PRINTING URL TO WEBPAGE

    job_page_source = requests.get(job.get("href"), headers=headers)  # REQUESTING HTML FOR SPECIFIC JOB WEB PAGE
    disposable_soup = BeautifulSoup(job_page_source.text, "lxml")  
    # MULTIPLE ELEMENTS ON THIS PAGE SHARE THE SAME TAG AND CLASS NAME. TURNING ALL ELEMENTS INTO LIST TO SORT BY INDEX
    page_content = disposable_soup.findAll("dd", class_="AdvortoDefinitionListElement AdvortoDefinitionListElementInline AdvortoDefinitionListAlternateItem")
    print(f"{page_content[1].text}\n{page_content[2].text}\n")  

    job_count += 1

print(f"QAapprenticeships Job Count = {job_count}")


# NOWSKILLS
# html_text = retrieve_html(website_addresses["nowskills"])
# job_count = 0

# for job in html_text.findAll("div", class_="nas-vacancy"):
#     if keyword not in job.h3.a.text.lower():
#         continue  
#     print(f"job title: {job.h3.a.text}")  # PRINTING THE JOB TITLE)
#     href = job.h3.a.get("href")
#     print(f"href = {href}")  # PRINTING URL JOB WEB PAGE
#     print(job.find("div", {"class"="nas-vacancy-date"}).text)
    
#     <div class="job-information_wrapper">
#     job_page_source = requests.get(href, headers=headers)  # IN ORDER TO OBTAIN POSTCODE & APPLICATION DEADLINE
#     disposable_soup = BeautifulSoup(job_page_source.text, "lxml")
#     print(disposable_soup.find("p", itemprop="postalCode").text)
#     print(disposable_soup.find("p", id="vacancy-closing-date").text)
#     print()

# job_count += 1