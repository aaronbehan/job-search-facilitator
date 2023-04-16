from bs4 import BeautifulSoup
import requests

# HEADER NECESSARY TO BYPASS BLOCKING FUNCTIONALITY OF CERTAIN WEBSITES
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}


def retrieve_html(url):
    main_page_source = requests.get(url, headers=header)
    soup = BeautifulSoup(main_page_source.text, "lxml")

    return soup


# ENTERING PARAMETRES
print("Aaron's Job Search Facilitator! Press ^C to kill program in terminal.")
keyword = input("Enter a jobsearch keyword>").strip()
postcode = input("Enter a postcode>").strip()
postcode_half1 = postcode[:3]
postcode_half2 = postcode[-3:]
distance = input("Enter distance in miles>")

# ADD TOTAL JOBS AND INDEED TO INCREASE 
website_addresses = [f"https://www.findapprenticeship.service.gov.uk/apprenticeships?SearchField=All&Keywords={keyword}&Location={postcode_half1}%20{postcode_half2}&WithinDistance={distance}&ApprenticeshipLevel=All&DisabilityConfidentOnly=false&Latitude=0&Longitude=0&Hash=-1210955484&SearchMode=Keyword&Category=&LocationType=NonNational&GoogleMapApiKey=0&sortType=Relevancy&SearchAction=Sort&resultsPerPage=10&DisplayDescription=true&DisplayDistance=true&DisplayClosingDate=true&DisplayStartDate=true&DisplayApprenticeshipLevel=false&DisplayWage=false"]

for website in website_addresses:
    html_text = retrieve_html(website)
    job_count = 0

    for job in html_text.findAll("li", class_="search-result sfa-section-bordered"):
        href = "https://www.findapprenticeship.service.gov.uk/" + job.h2.a.get("href")
        print(job.h2.a.text)  # PRINTING THE JOB TITLE)
        print(href)  # PRINTING URL TO SPECIFIC JOB WEB PAGE
        print(job.ul.li.text)  # PRINTING EMPLOYER
        job_page_source = requests.get(href, headers=header)  # IN ORDER TO OBTAIN POSTCODE & APPLICATION DEADLINE
        disposable_soup = BeautifulSoup(job_page_source.text, "lxml")
        print(disposable_soup.find("p", itemprop="postalCode").text)
        print(disposable_soup.find("p", id="vacancy-closing-date").text)
        print()
    
        job_count += 1
    
    print(f"Job Count: {job_count}")
