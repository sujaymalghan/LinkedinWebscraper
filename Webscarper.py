#Sujay vishwanath Malghan March 3 2023
###############################
import time
import random
import pandas as pd
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

email1=''
password1=''
with open('D:\python\input.txt', 'r', encoding='utf-8') as input_file:
    
    for line in input_file:
        line = line.strip()
        email1, password1 = line.split(':')

driver = webdriver.Chrome('C:\Drivers\driver\chromedriver.exe')

driver.get('https://www.linkedin.com/')


email = driver.find_element(by='name', value='session_key')
email.send_keys(email1)
password = driver.find_element(by='name', value='session_password')
password.send_keys(password1)
password.submit()

time.sleep(5)

driver.get('https://www.linkedin.com/in/sujay-malghan-74404a106/')

for i in range(1, 3):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(random.uniform(2, 4))


src = driver.page_source
soup1 = BeautifulSoup(src, 'lxml')






with open('D:\python\index.html', 'r') as f:
    contents = f.read()
with open('D:\python\job.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile,escapechar='\t' ,quoting=csv.QUOTE_NONE)
    try:
        name = soup1.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'})
        tiltedesc= soup1.find('div',{'class':'text-body-medium break-words'})
        location = soup1.find('span', {'class': 'text-body-small inline t-black--light break-words'})
        writer.writerow(["Subject Name: " + name.text.strip()])
        writer.writerow(["Title Description: " + tiltedesc.text.strip()])
        writer.writerow(["Location: " + location.text.strip()])
    except Exception as e:
        writer.writerow(["Not available"])
    try:
        about= soup1.find('div',{'class':'pv-shared-text-with-see-more full-width t-14 t-normal t-black display-flex align-items-center'}).find('span',{'aria-hidden':'true'})
        writer.writerow(["About: " + about.text.strip()])
    except Exception as e:
        writer.writerow(["Not available"])


    writer.writerow([])
    e = soup1.find("div", {"id": "experience"}).find_next('div',{'class':'pvs-list__outer-container'}).find('ul')
    writer.writerow(["Experience"])
    for entry in e.find_all('li'):
        try:
            div = entry.find('div', {'class': 'pvs-entity pvs-entity--padded pvs-list__item--no-padding-in-columns'})
            if div is not None:
                spans = div.find_all('span', {'aria-hidden': 'true'})
                row = []
                for i, label in enumerate(["Position", "Company", "Date Range", "Job Location", "Description"]):
                    if i < len(spans) and spans[i] is not None:
                        values=[spans[i].text.strip()]
                        writer.writerow([label + ": "+ spans[i].text.strip()])
                writer.writerow([])
        except IndexError:
            continue
        except AttributeError:
            continue
    
    try:
        if soup1.find("div", {"id": "education"}).find_next('div',{'class':'pvs-list__outer-container'}).find('ul') is not None:
            writer.writerow(["Education"]) 
            edu = soup1.find("div", {"id": "education"}).find_next('div',{'class':'pvs-list__outer-container'}).find('ul')
            for entry in edu.find_all('li'):
                try:
                    if entry.find('div',{'class':'pvs-entity pvs-entity--padded pvs-list__item--no-padding-in-columns'}) is not None:
                        if entry.find('div',{'class':'pvs-entity pvs-entity--padded pvs-list__item--no-padding-in-columns'}).find_all('span',{'aria-hidden':'true'})[0] is not None:    
                            writer.writerow(["Name of the school: " +  entry.find('div',{'class':'pvs-entity pvs-entity--padded pvs-list__item--no-padding-in-columns'}).find_all('span',{'aria-hidden':'true'})[0].text.strip()])
                        if entry.find('div',{'class':'pvs-entity pvs-entity--padded pvs-list__item--no-padding-in-columns'}).find_all('span',{'aria-hidden':'true'})[1] is not None:    
                            writer.writerow(["Degree: " + entry.find('div',{'class':'pvs-entity pvs-entity--padded pvs-list__item--no-padding-in-columns'}).find_all('span',{'aria-hidden':'true'})[1].text.strip()])
                        if entry.find('div',{'class':'pvs-entity pvs-entity--padded pvs-list__item--no-padding-in-columns'}).find_all('span',{'aria-hidden':'true'})[2] is not None:    
                            writer.writerow(["Date Range: " + entry.find('div',{'class':'pvs-entity pvs-entity--padded pvs-list__item--no-padding-in-columns'}).find_all('span',{'aria-hidden':'true'})[2].text.strip()])
                        if entry.find('div',{'class':'pvs-entity pvs-entity--padded pvs-list__item--no-padding-in-columns'}).find_all('span',{'aria-hidden':'true'})[3] is not None:    
                            writer.writerow(["Description: " + entry.find('div',{'class':'pvs-entity pvs-entity--padded pvs-list__item--no-padding-in-columns'}).find_all('span',{'aria-hidden':'true'})[3].text.strip()])
                            writer.writerow([])
                except IndexError:
                    continue
                except AttributeError:
                    continue
    except IndexError:
        print("Education section not found.")
    except AttributeError:
        print("Education section not found.")


   
    try:
        rec_container = soup1.find("div", {"id": "recommendations"}).find_next('div',{'class':'pvs-list__outer-container'})
        writer.writerow(["Recommendations"])
        if rec_container and rec_container.find('ul'):
            rec = rec_container.find('ul')
            entries = rec.find_all('li')
            for entry in entries:
                try:
                    entity = entry.find('div',{'class':'pvs-entity pvs-entity--padded pvs-list__item--no-padding-in-columns'})
                    spans = entity.find_all('span',{'aria-hidden':'true'})
                    name = spans[0].text.strip() if spans[0] else None
                    link = entry.find('a',{'class':'optional-action-target-wrapper display-flex'}).get('href') if entry.find('a',{'class':'optional-action-target-wrapper display-flex'}) else None
                    date = spans[3].text.strip()[:spans[3].text.strip().find(",", spans[3].text.strip().find(",") + 1)] if spans[3] else None
                    description = spans[3].text.strip()[spans[3].text.strip().find(",", spans[3].text.strip().find(",") + 1):] if spans[3] else None
                    testimonial = spans[4].text.strip() if spans[4] else None
                    writer.writerow(["Name" +": "+name])
                    writer.writerow(["Link" +": "+ link])
                    writer.writerow(["Date of testimonial" +": "+date])
                    writer.writerow(["Description of relationship" +":" +description])
                    writer.writerow(["Testimonial" +": "+testimonial])
                except IndexError:
                    continue
                except AttributeError:
                    continue
    except AttributeError:
        print("Recommendations section not found.")
        
    writer.writerow([])
    writer.writerow(["Projects"])
    try:
        project_container = soup1.find("div", {"id": "projects"}).find_next('div',{'class':'pvs-list__outer-container'})
        if project_container and project_container.find('ul'):
            projects = project_container.find('ul')
            entries = projects.find_all('li')    
            for entry in entries:
                try:
                    entity = entry.find('div',{'class':'pvs-entity pvs-entity--padded pvs-list__item--no-padding-in-columns'})
                    spans = entity.find_all('span',{'aria-hidden':'true'})
                    name = spans[0].text.strip() if spans[0] else None
                    dates = spans[1].text.strip() if spans[1] else None
                    association = spans[2].text.strip() if spans[2] else None
                    about = spans[3].text.strip() if spans[3] else None

                    writer.writerow(["Project Name: "+ name])
                    writer.writerow(["Dates: "+ dates])
                    writer.writerow(["Association: "+ association])
                    writer.writerow(["About: "+ about])
                    writer.writerow([])
                except AttributeError:
                    continue
                except IndexError:
                    continue
    except AttributeError:
        print("No projects section found")
driver.quit()

