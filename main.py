from Sandbpx1 import PageScraper
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# from sandbox import Scraper
import json
import time 
from time import sleep
from bs4 import BeautifulSoup

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--kiosk-printing')
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument('--headless')

# Set download directory
path_ = os.path.join(os.getcwd(), 'download')
prefs = {"download.default_directory": path_}
chrome_options.add_experimental_option("prefs", prefs)

# Create Chrome driver with the specified options
driver = webdriver.Chrome(options=chrome_options)

def Scaped_allPages():
    url = 'https://franchisesuppliernetwork.com/'
    scraper = PageScraper(webdriver)
    header_links = scraper.home_page_header_links(url)
    print(header_links)

    home_data = ""
    assessmentdata = ""
    FNSSupplierdata = ""
    financialData = ""
    humanResourceData = ""
    marketingData = ""
    operationData = ""
    realestateData = ""
    legalData = ""
    resourcedata = ""
    aboutData = ""
    contactData = ""

    for links in header_links:
        link = links['header_link']
        if link == url:
            home_data = scraper.scrape_home_page(link)
        elif 'com/assessment/' in link:
            assessmentdata =  scraper.scrape_assessment(link)
        elif link == "https://franchisesuppliernetwork.com/fsn-suppliers/":
            FNSSupplierdata =  scraper.scrape_FSN_suppliers(link)
        elif '.com/fsn-suppliers/financial-services/' in link:
            # print('financial-services:-',link)
            financialData  = scraper.scrape_financial_services(link)
        elif '.com/fsn-suppliers/human-resources-services/' in link:
            # print('human-resources:-',link)
            humanResourceData = scraper.scrape_human_resource_services(link)
        elif '.com/fsn-suppliers/marketing-services/' in link:
            # print('marketing-services:-',link)
            marketingData  = scraper.scrape_marketing_services(link)
        elif '.com/fsn-suppliers/operation-services/' in link:
            # print(link)
            operationData = scraper.scrape_opertation_services(link)
        elif 'com/fsn-suppliers/real-estate-services/' in link:
            # print(link)
            realestateData = scraper.scrape_real_estate_services(link)
        elif 'com/fsn-suppliers/legal-services/' in link:
            # print(link)
            legalData = scraper.scrape_legal_services(link)
        elif '.com/resources/' in link:
            # print(link)
            resourcedata = scraper.scrape_resources(link)
        elif '.com/about/' in link:
            # print(link)
            aboutData = scraper.scrape_about(link)
        elif '.com/contact/' in link:
            # print(link)
            contactData = scraper.scrape_contact(link)


    all_data = {
        'Home':home_data,
        'Assessment': assessmentdata,
        'FNSSupplier': FNSSupplierdata,
        'Financial': financialData,
        'HumanResource': humanResourceData,
        'Marketing': marketingData,
        'Operation': operationData,
        'RealEstate': realestateData,
        'Legal': legalData,
        'Resource': resourcedata,
        'About': aboutData,
        'Contact': contactData
    }

    # Write the combined data to a JSON file
    with open('combined_data.json', 'w') as json_file:
        json.dump(all_data, json_file, indent=4)

def scraped_FNSSupplied_and_homescrappedLinks():
    with open('FNSSuppliedScraped_data.json', 'r') as file1:
        data1 = json.load(file1)
    with open('HomeScraped_data.json', 'r') as file2:
        data2 = json.load(file2)

    urls1 = [item['CategoryUrl'] for item in data1['FNS Supplier']['Category']]
    urls2 = [item['FeatureURL'] for item in  data2['Home']['FeatureSection']['CategoryList']]
    all_urls = urls1 + urls2   
    unique_urls = list(set(all_urls))

    
    Main_data = []
    

    for url in unique_urls:
        combined_data = {}
        print('NewURL:-',url)
        driver.get(url)
        sleep(7)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser') 
        
        headers = image_div = soup.find('div', class_='col-xl-2 col-md-2 col-5')
        Header_image_url = image_div.find('img')['src']
        text_div = soup.find('div', class_='col-xl-3 col-md-5 col-12')
        Header_text = text_div.find('h2').text.strip()

        combined_data["Header"] ={
            "MainURL": url,
            'HeaderImage': Header_image_url,
            'HeaderText': Header_text
        }


        finalLists = []
        data_dict = {}
        fs_col_inns = soup.find_all('div', class_='col-lg-4 fs-col')

        for fs_col_inn in fs_col_inns:
            about_heading = fs_col_inn.find('h2').text.strip() 

            smallquestions = []
            if "Highlights" in about_heading:        
                small_q = fs_col_inn.find_all('h3')
                for questions in small_q:
                    question = questions.get_text(strip=True)
                    smallquestions.append(question)
            
            paragraph = []
            all_paragraphs = fs_col_inn.find_all('p')
            for p in all_paragraphs:
                Paragraph = p.get_text(strip=True)
                paragraph.append(Paragraph)

            alllink = []
            all_links = fs_col_inn.find_all('a')
            for link in all_links:
                link =  link['href']
                alllink.append(link)
                
            finalLists.append({
                "Header": about_heading,
                "Questions": smallquestions,
                "Paragraph": paragraph,
                "Link": alllink
            })
            # data_dict = {
            #     "About_Heading": about_heading,
            #     "Questions": smallquestions,
            #     "Paragraph": paragraph,
            #     "Link": alllink
            # }

        combined_data["SectionOne"] = {
            "FisrtSectionData": finalLists
        }

        # Extract Industries
        finalListsnext = []
        data_dict_next = {}
        innercontent = soup.find('div', class_='col-md-12')
        All_header = innercontent.find_all('div', class_='row fs-content-row')

        for fs_col_inn in All_header:
            header_text = ""
            AllLI = []            
            li = fs_col_inn.find_all('li')
            for lis in li:
                industry_name = lis.text.strip()
                AllLI.append(industry_name)
            # print('litag:-',AllLI)
            
            AllP = []       
            ptagdata = fs_col_inn.find_all('p')
            for P_tag in ptagdata:
                Paragraph = P_tag.text.strip()
                AllP.append(Paragraph)
            # print('AllP:- ',AllP)
            
            alllink = []    
            all_links = fs_col_inn.find_all('a')
            for link in all_links:
                link =  link['href']
                if not "javascript:;" in link:
                    alllink.append(link)   
            # print('alllink:-',alllink)

            Iframe = [] 
            iframe_tags = fs_col_inn.find_all('iframe')
            for iframe in iframe_tags:
                src_value = iframe['src']
                Iframe.append(src_value)
            # print('Iframe:-',Iframe)

            AllDIV = []
            content_main_div = fs_col_inn.find('div', id='contentMain')
            if content_main_div:
                text_content = content_main_div.text.strip()
                AllDIV.append(text_content)
            # print('AllDIV:-',AllDIV)

            finalListsnext.append({
            "Header": AllP,
            "IndustryName": AllLI,
            "Link": alllink,
            "YoutubeLink": Iframe,
            "Description": AllDIV
            })

            # data_dict_next = {            
            #     "Header": AllP,
            #     "IndustryName": AllLI,
            #     "Link": alllink,
            #     "YoutubeLink": Iframe,
            #     "Description": AllDIV
            # }
            
        combined_data["SectionTwo"] ={
            "SecondSectionData": finalListsnext
        }    
        Main_data.append(combined_data)

    json_data = json.dumps(Main_data, indent=4)

    # Write the JSON data to a file
    with open('FNSCategory_Data.json', 'w') as f:
        f.write(json_data)

def scraped_Resource_URLs():
    with open('ResourcesScraped_data.json', 'r') as file:
        data = json.load(file)

    urls = [item['CategoryUrl'] for item in data['Resources']['Category']]
    unique_urls = list(set(urls))
    # print(unique_urls)

    Main_data = []
    for url in unique_urls:
        combined_data = {}
        driver.get(url)
        sleep(7)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser') 

        url_content = soup.find('section', class_='contentside')   
        time_text = ""
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@ section one
        Header_text = url_content.find('h1').text.strip()
        username = url_content.find('div', class_='post_info').find(class_='author')
        username = username.text.strip()
        text_time = url_content.find('div', class_='post_info').find('time')
        if text_time:
            time_text = text_time.get_text(strip=True)

        combined_data["Header"] ={
            "MainURL": url,
            'HeaderText': Header_text,            
            'UserName': username,
            "Time": time_text
        }

        finalLists = []
        data_dict = {}
        # @@@@@@@@@@@@@@@@@@@@ section 2 image and paragraph
        maintag = url_content.find('div',class_='row')
        image_url = maintag.find('img')['src']
        # print(image_url)
        seperate_tag = maintag.find_all('div',class_='col-sm-12')
        for all_P in seperate_tag:
            
            allHeader = []    
            all_header = all_P.find_all('h2')
            for header in all_header:
                header = header.text.strip()
                allHeader.append(header)
            # print(allHeader)
            
            AllP = []       
            ptagdata = all_P.find_all('p')
            for P_tag in ptagdata:
                Paragraph = P_tag.text.strip()
                AllP.append(Paragraph)
            # print(AllP)
            
            alllink = []    
            all_links = all_P.find_all('a')
            for link in all_links:
                link =  link['href']
                if not "javascript:;" in link:
                    alllink.append(link) 
            # print(alllink)

            finalLists.append({
            "Header": allHeader,
            "Paragraph": AllP,
            "Link": alllink
            })
        combined_data["Information"] ={
            "ImageURL": image_url,
            "InformationSectionData": finalLists
        } 


        Main_data.append(combined_data)
    
    print('Main_data_:-',Main_data)
    json_data = json.dumps(Main_data, indent=4)

    # Write the JSON data to a file
    with open('ResourceCategory_Data.json', 'w') as f:
        f.write(json_data)



# scraped_FNSSupplied_and_homescrappedLinks()
scraped_Resource_URLs()
